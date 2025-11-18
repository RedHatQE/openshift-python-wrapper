"""Parser for OpenAPI explain data to extract resource information."""

from typing import Any

from simple_logger.logger import get_logger

from class_generator.constants import MISSING_DESCRIPTION_STR
from class_generator.core.schema import extract_group_kind_version, read_resources_mapping_file
from class_generator.parsers.type_parser import get_property_schema, prepare_property_dict
from class_generator.utils import get_latest_version
from ocp_resources.resource import Resource

LOGGER = get_logger(name=__name__)


class ResourceNotFoundError(Exception):
    """Raised when a resource kind is not found in the schema definition."""

    def __init__(self, kind: str) -> None:
        self.kind = kind
        super().__init__(f"Resource kind '{kind}' not found in schema definition")


def parse_explain(kind: str) -> list[dict[str, Any]]:
    """
    Parse OpenAPI explain data for a given resource kind.

    Args:
        kind: The Kubernetes resource kind

    Returns:
        List of resource dictionaries with parsed information
    """
    _schema_definition = read_resources_mapping_file()
    _resources: list[dict[str, Any]] = []

    # Check if the kind exists in the schema definition
    kind_lower = kind.lower()
    if kind_lower not in _schema_definition:
        raise ResourceNotFoundError(kind)

    _kinds_schema = _schema_definition[kind_lower]

    # Group schemas by API group
    schemas_by_group: dict[str, list[dict[str, Any]]] = {}
    for schema in _kinds_schema:
        gvk_list = schema.get("x-kubernetes-group-version-kind", [])
        if gvk_list:
            # Prefer non-empty groups over empty groups to avoid duplicates
            preferred_gvk = next((gvk for gvk in gvk_list if gvk.get("group")), gvk_list[0])
            group = preferred_gvk.get("group", "")
            if group not in schemas_by_group:
                schemas_by_group[group] = []
            schemas_by_group[group].append(schema)

    # For each API group, select the latest version
    filtered_schemas = []
    for _group, group_schemas in schemas_by_group.items():
        if len(group_schemas) > 1:
            # Multiple versions in same group - pick latest
            versions = []
            for schema in group_schemas:
                gvk_list = schema.get("x-kubernetes-group-version-kind", [])
                if gvk_list:
                    # Use same preference logic as grouping
                    preferred_gvk = next((gvk for gvk in gvk_list if gvk.get("group")), gvk_list[0])
                    version = preferred_gvk.get("version", "")
                    versions.append(version)

            latest_version = get_latest_version(versions=versions)

            # Add only the schema with the latest version
            for schema in group_schemas:
                gvk_list = schema.get("x-kubernetes-group-version-kind", [])
                if gvk_list:
                    # Use same preference logic as grouping
                    preferred_gvk = next((gvk for gvk in gvk_list if gvk.get("group")), gvk_list[0])
                    if preferred_gvk.get("version") == latest_version:
                        filtered_schemas.append(schema)
                        break
        else:
            # Single version in this group
            filtered_schemas.extend(group_schemas)

    # Use filtered schemas instead of all schemas
    for _kind_schema in filtered_schemas:
        # Validate 'namespaced' key exists
        if "namespaced" not in _kind_schema:
            LOGGER.warning(
                f"Schema for kind '{kind}' is missing 'namespaced' key. "
                f"Defaulting to namespaced=True. Schema: {_kind_schema.get('x-kubernetes-group-version-kind', [])}"
            )
            namespaced = True  # Default to namespaced resource
        else:
            namespaced = _kind_schema["namespaced"]

        resource_dict: dict[str, Any] = {
            "base_class": "NamespacedResource" if namespaced else "Resource",
            "description": _kind_schema.get("description", MISSING_DESCRIPTION_STR),
            "fields": [],
            "spec": [],
        }

        schema_properties: dict[str, Any] = _kind_schema.get("properties", {})
        fields_required = _kind_schema.get("required", [])

        resource_dict.update(extract_group_kind_version(kind_schema=_kind_schema))

        if spec_schema := schema_properties.get("spec", {}):
            spec_schema = get_property_schema(property_=spec_schema)
            spec_required = spec_schema.get("required", [])
            resource_dict = prepare_property_dict(
                schema=spec_schema.get("properties", {}),
                required=spec_required,
                resource_dict=resource_dict,
                dict_key="spec",
            )

        resource_dict = prepare_property_dict(
            schema=schema_properties,
            required=fields_required,
            resource_dict=resource_dict,
            dict_key="fields",
        )

        api_group_real_name = resource_dict.get("group")
        # Store the original group name before converting
        resource_dict["original_group"] = api_group_real_name

        # If API Group is not present in resource, try to get it from VERSION
        if not api_group_real_name:
            version_splited = resource_dict["version"].split("/")
            if len(version_splited) == 2:
                api_group_real_name = version_splited[0]
                resource_dict["original_group"] = api_group_real_name

        if api_group_real_name:
            api_group_for_resource_api_group = api_group_real_name.upper().replace(".", "_").replace("-", "_")
            resource_dict["group"] = api_group_for_resource_api_group
            missing_api_group_in_resource: bool = not hasattr(Resource.ApiGroup, api_group_for_resource_api_group)

            if missing_api_group_in_resource:
                LOGGER.warning(
                    f"Missing API Group in Resource\n"
                    f"Please add `Resource.ApiGroup.{api_group_for_resource_api_group} = {api_group_real_name}` "
                    "manually into ocp_resources/resource.py under Resource class > ApiGroup class."
                )

        else:
            api_version_for_resource_api_version = resource_dict["version"].upper()
            missing_api_version_in_resource: bool = not hasattr(
                Resource.ApiVersion, api_version_for_resource_api_version
            )

            if missing_api_version_in_resource:
                LOGGER.warning(
                    f"Missing API Version in Resource\n"
                    f"Please add `Resource.ApiVersion.{api_version_for_resource_api_version} = {resource_dict['version']}` "
                    "manually into ocp_resources/resource.py under Resource class > ApiVersion class."
                )

        _resources.append(resource_dict)

    return _resources
