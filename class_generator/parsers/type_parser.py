"""Parser for type generation and property parsing from OpenAPI schemas."""

import json
import textwrap
from pathlib import Path
from typing import Any

from simple_logger.logger import get_logger

from class_generator.constants import MISSING_DESCRIPTION_STR, SCHEMA_DIR, SPEC_STR
from class_generator.utils import sanitize_python_name
from ocp_resources.utils.utils import convert_camel_case_to_snake_case

LOGGER = get_logger(name=__name__)


def types_generator(key_dict: dict[str, Any]) -> dict[str, str]:
    """
    Generate type information for a property.

    Args:
        key_dict: Property schema dictionary

    Returns:
        Dictionary with type information for init and documentation
    """
    type_for_docstring: str = "Any"
    type_from_dict_for_init: str = ""
    # A resource field may be defined with `x-kubernetes-preserve-unknown-fields`. In this case, `type` is not provided.
    resource_type = key_dict.get("type")

    # All fields must be set with Optional since resource can have yaml_file to cover all args.
    if resource_type == "array":
        type_for_docstring = "list[Any]"

    elif resource_type == "string":
        type_for_docstring = "str"
        type_from_dict_for_init = f"{type_for_docstring} | None = None"

    elif resource_type == "boolean":
        type_for_docstring = "bool"

    elif resource_type == "integer":
        type_for_docstring = "int"

    elif resource_type == "object":
        type_for_docstring = "dict[str, Any]"

    if not type_from_dict_for_init:
        type_from_dict_for_init = f"{type_for_docstring} | None = None"

    return {"type-for-init": type_from_dict_for_init, "type-for-doc": type_for_docstring}


def get_property_schema(property_: dict[str, Any]) -> dict[str, Any]:
    """
    Resolve property schema, following $ref if needed.

    Args:
        property_: Property dictionary that may contain $ref

    Returns:
        Resolved property schema
    """
    # Handle direct $ref
    if _ref := property_.get("$ref"):
        # Extract the definition name from the $ref
        # e.g., "#/definitions/io.k8s.api.core.v1.PodSpec" -> "io.k8s.api.core.v1.PodSpec"
        # or "#/components/schemas/io.k8s.api.core.v1.PodSpec" -> "io.k8s.api.core.v1.PodSpec"
        ref_name = _ref.split("/")[-1]

        # Load from _definitions.json instead of individual files
        definitions_file = Path(SCHEMA_DIR) / "_definitions.json"
        if definitions_file.exists():
            with open(definitions_file) as fd:
                data = json.load(fd)
                definitions = data.get("definitions", {})
                if ref_name in definitions:
                    return definitions[ref_name]

        # Fallback to the property itself if ref not found
        LOGGER.warning(f"Could not resolve $ref: {_ref}")

    # Handle allOf containing $ref
    elif all_of := property_.get("allOf"):
        # allOf is typically used with a single $ref in Kubernetes schemas
        for item in all_of:
            if "$ref" in item:
                return get_property_schema(item)

    return property_


def format_description(description: str) -> str:
    """Format description text for documentation."""
    _res = ""
    _text = textwrap.wrap(text=description, subsequent_indent="    ")
    for _txt in _text:
        _res += f"{_txt}\n"

    return _res


def prepare_property_dict(
    schema: dict[str, Any],
    required: list[str],
    resource_dict: dict[str, Any],
    dict_key: str,
) -> dict[str, Any]:
    """
    Prepare property dictionary for template rendering.

    Args:
        schema: Schema properties
        required: List of required property names
        resource_dict: Resource dictionary to update
        dict_key: Key to update in resource_dict ("spec" or "fields")

    Returns:
        Updated resource dictionary
    """
    keys_to_ignore: list[str] = ["kind", "apiVersion", "status", SPEC_STR.lower()]
    keys_to_rename: set[str] = {"annotations", "labels"}
    if dict_key != SPEC_STR.lower():
        keys_to_ignore.append("metadata")

    for key, val in schema.items():
        if key in keys_to_ignore:
            continue

        val_schema = get_property_schema(property_=val)
        type_dict = types_generator(key_dict=val_schema)
        python_name = convert_camel_case_to_snake_case(name=f"{dict_key}_{key}" if key in keys_to_rename else key)

        # Sanitize Python reserved keywords
        safe_python_name, original_name = sanitize_python_name(name=python_name)
        is_keyword_renamed = safe_python_name != original_name

        resource_dict[dict_key].append({
            "name-for-class-arg": safe_python_name,
            "property-name": key,
            "original-python-name": python_name,  # Store original for reference
            "is-keyword-renamed": is_keyword_renamed,  # Flag for template
            "required": key in required,
            "description": format_description(description=val_schema.get("description", MISSING_DESCRIPTION_STR)),
            "type-for-docstring": type_dict["type-for-doc"],
            "type-for-class-arg": f"{safe_python_name}: {type_dict['type-for-init']}",
        })

    return resource_dict
