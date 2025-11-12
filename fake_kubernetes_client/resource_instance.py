"""FakeResourceInstance implementation for fake Kubernetes client"""

import copy
import time
import uuid
from collections.abc import Iterator
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Union

from fake_kubernetes_client.exceptions import ConflictError, MethodNotAllowedError, NotFoundError
from fake_kubernetes_client.resource_field import FakeResourceField
from fake_kubernetes_client.status_templates import add_realistic_status

if TYPE_CHECKING:
    from fake_kubernetes_client.dynamic_client import FakeDynamicClient
    from fake_kubernetes_client.resource_storage import FakeResourceStorage

try:
    from kubernetes.client.rest import ApiException as K8sApiException
except ImportError:
    K8sApiException = None


class FakeResourceInstance:
    """Fake implementation of kubernetes.dynamic.client.ResourceInstance"""

    def __init__(
        self, resource_def: dict[str, Any], storage: "FakeResourceStorage", client: Union["FakeDynamicClient", None]
    ) -> None:
        self.resource_def = resource_def
        self.storage = storage
        self.client = client

    def _normalize_namespace(self, namespace: str | None) -> str | None:
        """Normalize namespace parameter (empty string -> None)"""
        return None if namespace == "" else namespace

    def _get_storage_api_version(self) -> str:
        """Get consistent API version for storage operations"""
        return self.resource_def.get("group_version", self.resource_def["api_version"])

    def _create_not_found_error(self, name: str) -> None:
        """Create proper NotFoundError with Kubernetes-style exception"""
        try:
            api_exception = K8sApiException(status=404, reason=f"{self.resource_def['kind']} '{name}' not found")
            raise NotFoundError(api_exception) from None
        except (NameError, TypeError):
            # K8sApiException not available (ImportError at module level)
            raise NotFoundError(f"{self.resource_def['kind']} '{name}' not found") from None

    def _create_conflict_error(self, name: str) -> None:
        """Create proper ConflictError with Kubernetes-style exception"""
        try:
            # ConflictError expects an ApiException as argument
            api_exception = K8sApiException(status=409, reason="AlreadyExists")
            api_exception.body = f'{{"kind":"Status","apiVersion":"v1","metadata":{{}},"status":"Failure","message":"{self.resource_def["kind"]} \\"{name}\\" already exists","reason":"AlreadyExists","code":409}}'
            raise ConflictError(api_exception) from None
        except (NameError, TypeError):
            # K8sApiException not available (ImportError at module level)
            # Use our fake ConflictError which has status attribute
            raise ConflictError(f"{self.resource_def['kind']} '{name}' already exists") from None

    def _generate_resource_version(self) -> str:
        """Generate unique resource version"""
        return str(int(time.time() * 1000))

    def _generate_timestamp(self) -> str:
        """Generate current UTC timestamp in ISO format"""
        return datetime.now(timezone.utc).isoformat()

    def create(
        self, body: dict[str, Any] | None = None, namespace: str | None = None, **_kwargs: Any
    ) -> FakeResourceField:
        """Create a resource"""
        if body is None:
            raise ValueError("body is required for create")

        # Validate body structure
        if not isinstance(body, dict):
            raise ValueError("body must be a dictionary")

        if "metadata" not in body:
            body["metadata"] = {}

        # Set namespace if provided - REQUIRE namespaced field to be present
        if namespace and self.resource_def.get("namespaced"):
            body["metadata"]["namespace"] = namespace

        # Generate metadata if not present
        if "name" not in body["metadata"]:
            raise ValueError("metadata.name is required")

        name = body["metadata"]["name"]
        resource_namespace = (
            body["metadata"].get("namespace", "default") if self.resource_def.get("namespaced") else None
        )

        # Use group_version for storage operations (consistent full API version)
        storage_api_version = self._get_storage_api_version()

        # Check if resource already exists
        existing = self.storage.get_resource(
            kind=self.resource_def["kind"], api_version=storage_api_version, name=name, namespace=resource_namespace
        )
        if existing:
            self._create_conflict_error(name)

        # Add generated metadata
        body["metadata"].update({
            "uid": str(uuid.uuid4()),
            "resourceVersion": self._generate_resource_version(),
            "creationTimestamp": self._generate_timestamp(),
            "generation": 1,
            "labels": body["metadata"].get("labels", {}),
            "annotations": body["metadata"].get("annotations", {}),
        })

        # Set API version and kind
        body["apiVersion"] = storage_api_version  # Use the same full API version for body
        body["kind"] = self.resource_def["kind"]

        # Add realistic status for resources that need it
        # Pass resource mappings from registry if available
        resource_mappings = None
        if self.client and hasattr(self.client, "registry"):
            resource_mappings = self.client.registry._get_resource_mappings()

        add_realistic_status(body=body, resource_mappings=resource_mappings)

        # Special case: ProjectRequest is ephemeral - only creates Project (matches real cluster behavior)
        if self.resource_def["kind"] == "ProjectRequest":
            # Don't store ProjectRequest - it's ephemeral
            project_body = self._create_corresponding_project(body)
            # Generate events for the Project creation, not ProjectRequest
            self._generate_resource_events(project_body, "Created", "created")
            # Return Project data, not ProjectRequest (ProjectRequest is ephemeral)
            return FakeResourceField(data=project_body)

        # Store resource with initial metadata and status
        self.storage.store_resource(
            api_version=storage_api_version,  # Use consistent API version for storage
            kind=self.resource_def["kind"],
            name=name,
            namespace=self._normalize_namespace(namespace),  # Normalize namespace (empty string -> None)
            resource=body,
        )

        # Generate automatic events for resource creation
        self._generate_resource_events(body, "Created", "created")

        return FakeResourceField(data=body)

    def _create_corresponding_project(self, project_request_body: dict[str, Any]) -> dict[str, Any]:
        """Create a corresponding Project when ProjectRequest is created (simulates real OpenShift behavior)"""
        project_name = project_request_body["metadata"]["name"]

        # Create Project with same name and similar metadata
        project_body = {
            "apiVersion": "project.openshift.io/v1",
            "kind": "Project",
            "metadata": {
                "name": project_name,
                "uid": str(uuid.uuid4()),
                "resourceVersion": self._generate_resource_version(),
                "creationTimestamp": self._generate_timestamp(),
                "generation": 1,
                "labels": project_request_body["metadata"].get("labels", {}),
                "annotations": project_request_body["metadata"].get("annotations", {}),
            },
            "spec": {"finalizers": ["kubernetes"]},
            "status": {"phase": "Active"},
        }

        # Store the Project (cluster-scoped resource)
        self.storage.store_resource(
            kind="Project",
            api_version="project.openshift.io/v1",
            name=project_name,
            namespace=None,  # Projects are cluster-scoped
            resource=project_body,
        )

        # Return the project body for use by create() method
        return project_body

    def _generate_resource_events(self, resource: dict[str, Any], reason: str, action: str) -> None:
        """Generate automatic events for resource operations - completely resource-agnostic"""
        if not resource or not resource.get("metadata"):
            return

        resource_name = resource["metadata"].get("name")
        resource_namespace = resource["metadata"].get("namespace")
        resource_kind = resource.get("kind")
        resource_uid = resource["metadata"].get("uid")

        if not resource_name or not resource_kind:
            return

        # Generate event name (Kubernetes pattern)
        event_name = f"{resource_name}.{int(time.time() * 1000000)}"

        # Create realistic event
        event = {
            "apiVersion": "v1",
            "kind": "Event",
            "metadata": {
                "name": event_name,
                "namespace": resource_namespace or "default",
                "uid": str(uuid.uuid4()),
                "resourceVersion": str(int(time.time() * 1000)),
                "creationTimestamp": datetime.now(timezone.utc).isoformat(),
                "generation": 1,
            },
            "involvedObject": {
                "apiVersion": resource.get("apiVersion"),
                "kind": resource_kind,
                "name": resource_name,
                "namespace": resource_namespace,
                "uid": resource_uid,
                "resourceVersion": resource["metadata"].get("resourceVersion"),
            },
            "reason": reason,
            "message": f"{resource_kind} {resource_name} has been {action}",
            "source": {"component": "fake-client", "host": "fake-cluster.example.com"},
            "firstTimestamp": datetime.now(timezone.utc).isoformat(),
            "lastTimestamp": datetime.now(timezone.utc).isoformat(),
            "count": 1,
            "type": "Normal",
        }

        # Store the event
        event_namespace = resource_namespace or "default"
        self.storage.store_resource(
            kind="Event", api_version="v1", name=event_name, namespace=event_namespace, resource=event
        )

    def get(
        self,
        name: str | None = None,
        namespace: str | None = None,
        label_selector: str | None = None,
        field_selector: str | None = None,
        **_kwargs: Any,
    ) -> FakeResourceField:
        """Get resource(s)"""
        if name:
            # Get specific resource
            namespace = self._normalize_namespace(namespace)

            # Use group_version for storage access (consistent full API version)
            storage_api_version = self._get_storage_api_version()
            resource = self.storage.get_resource(
                kind=self.resource_def["kind"], api_version=storage_api_version, name=name, namespace=namespace
            )
            if not resource:
                self._create_not_found_error(name)
            return FakeResourceField(data=resource)

        # List resources using consistent API version
        storage_api_version = self._get_storage_api_version()
        resources = self.storage.list_resources(
            kind=self.resource_def["kind"],
            api_version=storage_api_version,
            namespace=self._normalize_namespace(namespace),  # Normalize namespace here too
            label_selector=label_selector,
            field_selector=field_selector,
        )

        # Create list response
        response = {
            "apiVersion": self.resource_def["api_version"],
            "kind": f"{self.resource_def['kind']}List",
            "metadata": {
                "resourceVersion": self._generate_resource_version(),
            },
            "items": resources,
        }

        return FakeResourceField(data=response)

    def delete(
        self,
        name: str | None = None,
        namespace: str | None = None,
        _body: dict[str, Any] | None = None,
        **_kwargs: Any,
    ) -> FakeResourceField:
        """Delete resource(s)"""
        if name:
            # Delete specific resource
            namespace = self._normalize_namespace(namespace)

            storage_api_version = self._get_storage_api_version()
            deleted = self.storage.delete_resource(
                kind=self.resource_def["kind"], api_version=storage_api_version, name=name, namespace=namespace
            )
            if not deleted:
                self._create_not_found_error(name)
            # Generate automatic events for resource deletion
            if deleted:
                self._generate_resource_events(deleted, "Deleted", "deleted")

            return FakeResourceField(data=deleted if deleted else {})

        # Delete collection - not implemented for safety
        raise MethodNotAllowedError("Collection deletion not supported")

    def patch(
        self,
        name: str | None = None,
        body: dict[str, Any] | None = None,
        namespace: str | None = None,
        **_kwargs: Any,
    ) -> FakeResourceField:
        """Patch a resource"""
        if not body:
            raise ValueError("body is required for patch")

        # Extract name from body if not provided (like real Kubernetes client)
        if not name:
            name = body.get("metadata", {}).get("name")
            if not name:
                raise ValueError("name is required for patch")

        namespace = self._normalize_namespace(namespace)

        storage_api_version = self._get_storage_api_version()
        existing = self.storage.get_resource(
            kind=self.resource_def["kind"], api_version=storage_api_version, name=name, namespace=namespace
        )
        if not existing:
            self._create_not_found_error(name)
            # This line is unreachable but satisfies type checker
            return FakeResourceField(data={})

        # Simple merge patch implementation
        patched = copy.deepcopy(existing)
        self._merge_patch(patched, body)

        # Update metadata
        patched["metadata"]["resourceVersion"] = self._generate_resource_version()
        if "generation" in patched["metadata"]:
            patched["metadata"]["generation"] += 1

        # Store updated resource
        self.storage.store_resource(
            kind=self.resource_def["kind"],
            api_version=storage_api_version,
            name=name,
            namespace=namespace,
            resource=patched,
        )

        # Generate automatic events for resource patch
        self._generate_resource_events(patched, "Updated", "updated")

        return FakeResourceField(data=patched)

    def replace(
        self,
        name: str | None = None,
        body: dict[str, Any] | None = None,
        namespace: str | None = None,
        **_kwargs: Any,
    ) -> FakeResourceField:
        """Replace a resource"""
        if not name:
            raise ValueError("name is required for replace")
        if not body:
            raise ValueError("body is required for replace")

        namespace = self._normalize_namespace(namespace)

        storage_api_version = self._get_storage_api_version()
        existing = self.storage.get_resource(
            kind=self.resource_def["kind"], api_version=storage_api_version, name=name, namespace=namespace
        )
        if not existing:
            self._create_not_found_error(name)
            # This line is unreachable but satisfies type checker
            return FakeResourceField(data={})

        # Check for resourceVersion conflict - this is what Kubernetes does
        if "metadata" in body and "resourceVersion" in body["metadata"]:
            if body["metadata"]["resourceVersion"] != existing["metadata"]["resourceVersion"]:
                # Create conflict error with proper message
                try:
                    api_exception = K8sApiException(status=409, reason="Conflict")
                    api_exception.body = f'{{"kind":"Status","apiVersion":"v1","metadata":{{}},"status":"Failure","message":"Operation cannot be fulfilled on {self.resource_def["kind"].lower()}s.{self.resource_def.get("group", "")} \\"{name}\\": the object has been modified; please apply your changes to the latest version and try again","reason":"Conflict","code":409}}'
                    raise ConflictError(api_exception) from None
                except (NameError, TypeError):
                    # Use our fake ConflictError which has status attribute
                    raise ConflictError(
                        f"Operation cannot be fulfilled on {self.resource_def['kind']} '{name}': the object has been modified"
                    ) from None

        # Ensure metadata is preserved
        if "metadata" not in body:
            body["metadata"] = {}

        body["metadata"].update({
            "uid": existing["metadata"]["uid"],
            "resourceVersion": self._generate_resource_version(),
            "creationTimestamp": existing["metadata"]["creationTimestamp"],
            "generation": existing["metadata"].get("generation", 1) + 1,
        })

        # Set API version and kind
        body["apiVersion"] = self.resource_def["api_version"]
        body["kind"] = self.resource_def["kind"]

        # Store replaced resource
        self.storage.store_resource(
            kind=self.resource_def["kind"],
            api_version=storage_api_version,
            name=name,
            namespace=namespace,
            resource=body,
        )

        # Generate automatic events for resource replacement
        self._generate_resource_events(body, "Updated", "replaced")

        # Return the stored resource (which has the updated metadata)
        return FakeResourceField(
            data=self.storage.get_resource(
                kind=self.resource_def["kind"], api_version=storage_api_version, name=name, namespace=namespace
            )
        )

    def update(
        self,
        name: str | None = None,
        body: dict[str, Any] | None = None,
        namespace: str | None = None,
        **kwargs: Any,
    ) -> FakeResourceField:
        """Update a resource (alias for replace)"""
        return self.replace(name=name, body=body, namespace=namespace, **kwargs)

    def watch(
        self, namespace: str | None = None, _timeout: int | None = None, **kwargs: Any
    ) -> Iterator[dict[str, Any]]:
        """Watch for resource changes"""
        # Simple implementation - yields existing resources as ADDED events
        storage_api_version = self.resource_def.get("group_version", self.resource_def["api_version"])

        # Extract label and field selectors from kwargs
        label_selector = kwargs.get("label_selector")
        field_selector = kwargs.get("field_selector")

        resources = self.storage.list_resources(
            kind=self.resource_def["kind"],
            api_version=storage_api_version,
            namespace=self._normalize_namespace(namespace),  # Normalize namespace here too
            label_selector=label_selector,
            field_selector=field_selector,
        )

        for resource in resources:
            yield {"type": "ADDED", "object": FakeResourceField(data=resource), "raw_object": resource}

    def _merge_patch(self, target: dict[str, Any], patch: dict[str, Any]) -> None:
        """Simple merge patch implementation"""
        if isinstance(patch, dict):
            for key, value in patch.items():
                if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                    self._merge_patch(target[key], value)
                else:
                    target[key] = value
