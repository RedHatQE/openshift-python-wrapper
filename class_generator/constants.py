"""Constants used throughout the class generator."""

import keyword
import os

# String constants
SPEC_STR: str = "SPEC"
FIELDS_STR: str = "FIELDS"

# Directory constants
TESTS_MANIFESTS_DIR: str = "class_generator/tests/manifests"
SCHEMA_DIR: str = "class_generator/schema"
RESOURCES_MAPPING_FILE: str = os.path.join(SCHEMA_DIR, "__resources-mappings.json")

# Description constants
MISSING_DESCRIPTION_STR: str = "No field description from API"

# Python keyword mappings for safe variable names
PYTHON_KEYWORD_MAPPINGS = {
    # Map Python keywords to safe alternatives by appending underscore
    kw: f"{kw}_"
    for kw in keyword.kwlist
}

# Version priority for Kubernetes API versions
VERSION_PRIORITY = {
    "v2": 6,
    "v1": 5,
    "v1beta2": 4,
    "v1beta1": 3,
    "v1alpha2": 2,
    "v1alpha1": 1,
}

# Generated code marker
END_OF_GENERATED_CODE = "# End of generated code"
GENERATED_USING_MARKER = "# Generated using"
