"""FakeResourceRegistry implementation for fake Kubernetes client"""

import logging
from collections import defaultdict
from typing import Any

from fake_kubernetes_client.resource_field import FakeResourceField
from ocp_resources.utils.schema_validator import SchemaValidator

logger = logging.getLogger(__name__)


class FakeResourceRegistry:
    """Registry for resource definitions"""

    def __init__(self) -> None:
        # Store by kind to allow searching across API groups
        self.resources: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
        self._resource_mappings_cache: dict[str, Any] | None = None
        self._builtin_resources: dict[tuple[str, str], dict[str, Any]] = {}
        self._additional_resources: dict[str, list[dict[str, Any]]] = {}
        self._load_resource_definitions()
        self._register_additional_resources()

    def _generate_plural_form(self, kind: str) -> str:
        """Generate plural form of resource kind using standard Kubernetes rules"""
        kind_lower = kind.lower()
        if kind_lower.endswith("s"):
            return kind_lower
        elif kind_lower.endswith("y"):
            return kind_lower[:-1] + "ies"
        elif kind_lower.endswith(("sh", "ch", "x", "z")):
            return kind_lower + "es"
        else:
            return kind_lower + "s"

    def _get_resource_mappings(self) -> dict[str, Any]:
        """Load and cache the resource mappings file using SchemaValidator"""
        if self._resource_mappings_cache is None:
            # Use SchemaValidator to load the mappings - single source of truth
            if SchemaValidator.load_mappings_data():
                self._resource_mappings_cache = SchemaValidator.get_mappings_data() or {}
                logger.debug(f"Loaded {len(self._resource_mappings_cache)} resource mappings from SchemaValidator")
            else:
                logger.error("Failed to load resource mappings from SchemaValidator")
                self._resource_mappings_cache = {}

        return self._resource_mappings_cache

    def _apply_known_corrections(self, kind: str, resource_def: dict[str, Any]) -> dict[str, Any]:
        """Apply known corrections to resource definitions"""
        # Known corrections for incorrect data in the JSON file
        corrections = {
            # Service is incorrectly marked as non-namespaced in the JSON
            "Service": {"namespaced": True},
            # Event is incorrectly marked as non-namespaced in the JSON
            "Event": {"namespaced": True},
            # Add other known corrections here as needed
        }

        if kind in corrections:
            resource_def.update(corrections[kind])

        return resource_def

    def _load_resource_definitions(self) -> None:
        """Load resource definitions from JSON file - single source of truth"""
        mappings = self._get_resource_mappings()
        if not mappings:
            # If no mappings file found, registry will be empty
            # This will cause proper errors when resources are requested
            return

        for kind_lower, resource_mappings in mappings.items():
            if not isinstance(resource_mappings, list) or not resource_mappings:
                continue

            # Process all mappings for this kind (there might be multiple API groups)
            for mapping in resource_mappings:
                # Extract kubernetes metadata from x-kubernetes-group-version-kind
                k8s_gvk = mapping.get("x-kubernetes-group-version-kind", [])
                if not k8s_gvk or not isinstance(k8s_gvk, list) or not k8s_gvk:
                    continue

                # Process each group-version-kind entry
                for gvk in k8s_gvk:
                    schema_group = gvk.get("group", "")
                    schema_version = gvk.get("version")
                    schema_kind = gvk.get("kind", kind_lower.title())

                    # Skip if no version found in mappings
                    if not schema_version:
                        continue

                    # Build full API version
                    if schema_group:
                        full_api_version = f"{schema_group}/{schema_version}"
                    else:
                        full_api_version = schema_version

                    # Get namespace info from mappings
                    is_namespaced = mapping.get("namespaced")
                    if is_namespaced is None:
                        continue

                    # Generate plural form
                    plural = self._generate_plural_form(schema_kind)

                    resource_def = {
                        "kind": schema_kind,
                        "api_version": schema_version,  # Just version part for KubeAPIVersion compatibility
                        "group": schema_group,
                        "version": schema_version,
                        "group_version": full_api_version,  # Full group/version for storage operations
                        "plural": plural,
                        "singular": schema_kind.lower(),
                        "namespaced": is_namespaced,
                        "shortNames": [],
                        "categories": ["all"],
                        "schema_source": "mappings",
                    }

                    # Apply known corrections
                    resource_def = self._apply_known_corrections(schema_kind, resource_def)

                    # Store in both places for compatibility
                    self.resources[schema_kind].append(resource_def)
                    key = (full_api_version, schema_kind)
                    self._builtin_resources[key] = resource_def

    def _register_additional_resources(self) -> None:
        """Register additional resources that are not in OpenShift schema"""
        # MTQ resources (not in OpenShift schema)
        additional_resources = [
            {
                "kind": "MigrationToolkitQuota",
                "api_version": "v1alpha1",
                "group": "mtq.kubevirt.io",
                "version": "v1alpha1",
                "group_version": "mtq.kubevirt.io/v1alpha1",
                "plural": "migrationtoolkitquotas",
                "singular": "migrationtoolkitquota",
                "namespaced": False,
                "shortNames": ["mtq"],
                "categories": ["all"],
                "schema_source": "additional",
            },
            {
                "kind": "MTQ",
                "api_version": "v1alpha1",
                "group": "mtq.kubevirt.io",
                "version": "v1alpha1",
                "group_version": "mtq.kubevirt.io/v1alpha1",
                "plural": "mtqs",
                "singular": "mtq",
                "namespaced": False,
                "shortNames": [],
                "categories": ["all"],
                "schema_source": "additional",
            },
            {
                "kind": "Service",
                "api_version": "v1",
                "group": "serving.knative.dev",
                "version": "v1",
                "group_version": "serving.knative.dev/v1",
                "plural": "services",
                "singular": "service",
                "namespaced": True,
                "shortNames": ["ksvc"],
                "categories": ["all"],
                "schema_source": "additional",
            },
            {
                "kind": "PodMetrics",
                "api_version": "v1beta1",
                "group": "metrics.k8s.io",
                "version": "v1beta1",
                "group_version": "metrics.k8s.io/v1beta1",
                "plural": "podmetrics",
                "singular": "podmetrics",
                "namespaced": True,
                "shortNames": [],
                "categories": ["all"],
                "schema_source": "additional",
            },
            {
                "kind": "Image",
                "api_version": "v1alpha1",
                "group": "caching.internal.knative.dev",
                "version": "v1alpha1",
                "group_version": "caching.internal.knative.dev/v1alpha1",
                "plural": "images",
                "singular": "image",
                "namespaced": True,
                "shortNames": [],
                "categories": ["all"],
                "schema_source": "additional",
            },
        ]

        for resource_def in additional_resources:
            kind = str(resource_def["kind"])
            group_version = str(resource_def["group_version"])
            self.resources[kind].append(resource_def)
            key = (group_version, kind)
            self._builtin_resources[key] = resource_def
            self._additional_resources.setdefault(kind, []).append(resource_def)

    def register_resources(self, resources: dict[str, Any] | list[dict[str, Any]]) -> None:
        """
        Register custom resources dynamically.

        Args:
            resources: Either a single resource definition dict or a list of resource definitions.
                      Each resource definition should contain:
                      - kind: Resource kind (required)
                      - api_version: API version without group (required)
                      - group: API group (optional, empty string for core resources)
                      - version: Same as api_version (required)
                      - group_version: Full group/version string (required)
                      - plural: Plural name (optional, will be generated if not provided)
                      - singular: Singular name (optional, defaults to lowercase kind)
                      - namespaced: Whether resource is namespaced (optional, defaults to True)
                      - shortNames: List of short names (optional)
                      - categories: List of categories (optional, defaults to ["all"])

        Example:
            client.registry.register_resources({
                "kind": "MyCustomResource",
                "api_version": "v1alpha1",
                "group": "example.com",
                "version": "v1alpha1",
                "group_version": "example.com/v1alpha1",
                "plural": "mycustomresources",
                "singular": "mycustomresource",
                "namespaced": True,
                "shortNames": ["mcr"],
                "categories": ["all"]
            })
        """
        # Convert single resource to list for uniform processing
        resource_list = [resources] if isinstance(resources, dict) else resources

        for resource_def in resource_list:
            # Validate required fields
            if not isinstance(resource_def, dict):
                raise ValueError(f"Resource definition must be a dictionary, got {type(resource_def)}")

            kind = resource_def.get("kind", "")
            if not kind:
                raise ValueError("Resource definition must have 'kind' field")

            api_version = resource_def.get("api_version", "")
            if not api_version:
                raise ValueError(f"Resource {kind} must have 'api_version' field")

            # Build complete resource definition with defaults
            group = resource_def.get("group", "")
            version = resource_def.get("version", api_version)

            # Generate group_version if not provided
            if "group_version" not in resource_def:
                group_version = f"{group}/{version}" if group else version
            else:
                group_version = resource_def["group_version"]

            # Generate plural if not provided
            plural = resource_def.get("plural", self._generate_plural_form(kind))

            # Build complete resource definition
            complete_def = {
                "kind": kind,
                "api_version": api_version,
                "group": group,
                "version": version,
                "group_version": group_version,
                "plural": plural,
                "singular": resource_def.get("singular", kind.lower()),
                "namespaced": resource_def.get("namespaced", True),
                "shortNames": resource_def.get("shortNames", []),
                "categories": resource_def.get("categories", ["all"]),
                "schema_source": "user_defined",
            }

            # Register the resource
            self.resources[kind].append(complete_def)
            key = (str(group_version), str(kind))
            self._builtin_resources[key] = complete_def
            self._additional_resources.setdefault(kind, []).append(complete_def)

    def search(
        self,
        kind: str | None = None,
        group: str | None = None,
        api_version: str | None = None,
        **_kwargs: Any,
    ) -> list[FakeResourceField]:
        """Search for resource definitions"""
        results = []

        # If searching by kind and group, look for that specific combination
        if kind and group is not None:
            definitions = self.resources.get(kind, [])
            for definition in definitions:
                if definition.get("group") == group:
                    results.append(FakeResourceField(data=definition))
        else:
            # General search through all resources
            for resource_kind, definitions in self.resources.items():
                # Filter by kind if specified
                if kind and resource_kind != kind:
                    continue

                for definition in definitions:
                    # Filter by group if specified
                    if group and definition.get("group") != group:
                        continue
                    # Filter by api_version if specified
                    if api_version and definition.get("group_version") != api_version:
                        continue

                    results.append(FakeResourceField(data=definition))

        return results

    def get_resource_definitions(self, kind: str) -> list[dict[str, Any]]:
        """Get all resource definitions for a kind"""
        return self.resources.get(kind, [])

    def get_resource_definition(self, kind: str, api_version: str) -> dict[str, Any] | None:
        """Get specific resource definition by kind and API version"""
        definitions = self.resources.get(kind, [])

        # If api_version doesn't contain '/', it's a core resource (no group)
        if "/" not in api_version:
            # First, try to find a core resource (empty group) with this version
            for definition in definitions:
                if definition.get("group") == "" and definition["version"] == api_version:
                    return definition

            # If not found, fall back to checking group_version for compatibility
            for definition in definitions:
                if definition.get("group_version") == api_version:
                    return definition
        else:
            # API version contains group, do exact match on group_version
            for definition in definitions:
                if definition.get("group_version") == api_version:
                    return definition

        return None

    def get_resource_definition_by_plural(self, plural: str, api_version: str) -> dict[str, Any] | None:
        """Get resource definition by plural name and API version"""
        for _kind, definitions in self.resources.items():
            for definition in definitions:
                if definition.get("plural") == plural and (
                    definition["api_version"] == api_version or definition.get("group_version") == api_version
                ):
                    return definition
        return None

    def list_api_resources(self, api_version: str) -> FakeResourceField:
        """List all resources for an API version"""
        resources = []
        for kind, definitions in self.resources.items():
            for definition in definitions:
                # Check both api_version and group_version
                if definition["api_version"] == api_version or definition.get("group_version") == api_version:
                    resources.append({
                        "name": definition.get("plural", f"{kind.lower()}s"),
                        "singularName": definition.get("singular", kind.lower()),
                        "namespaced": definition.get("namespaced", True),
                        "kind": kind,
                        "verbs": ["create", "delete", "deletecollection", "get", "list", "patch", "update", "watch"],
                    })

        # Create APIResourceList response
        response = {
            "apiVersion": "v1",
            "groupVersion": api_version,
            "kind": "APIResourceList",
            "resources": resources,
        }

        return FakeResourceField(data=response)
