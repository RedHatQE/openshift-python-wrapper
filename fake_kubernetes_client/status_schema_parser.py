"""Status schema parser for generating dynamic status from resource schemas"""

import json
import os
import random
from datetime import datetime, timezone
from typing import Any


class StatusSchemaParser:
    """Parser for generating status from resource schemas"""

    def __init__(self, resource_mappings: dict[str, Any]) -> None:
        self.resource_mappings = resource_mappings
        self._definitions_cache: dict[str, Any] = {}
        self._definitions: dict[str, Any] = {}
        self._load_definitions()

    def _load_definitions(self) -> None:
        """Load the definitions file once"""
        definitions_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "class_generator",
            "schema",
            "_definitions.json",
        )

        if os.path.exists(definitions_path):
            with open(definitions_path) as f:
                data = json.load(f)
                self._definitions = data.get("definitions", {})

    def get_status_schema_for_resource(self, kind: str, _api_version: str) -> dict[str, Any] | None:
        """Get status schema for a specific resource"""
        kind_lower = kind.lower()
        resource_schemas = self.resource_mappings.get(kind_lower, [])

        if not resource_schemas:
            return None

        # Find the matching schema for the API version
        for schema in resource_schemas:
            gvk_list = schema.get("x-kubernetes-group-version-kind", [])
            for gvk in gvk_list:
                if gvk.get("kind") == kind:
                    # Found matching resource, check if it has status
                    properties = schema.get("properties", {})
                    status_ref = properties.get("status", {})

                    if "$ref" in status_ref:
                        # Resolve the reference to get actual status schema
                        return self._resolve_reference(status_ref["$ref"])
                    elif status_ref.get("type") == "object":
                        # Direct status object
                        return status_ref

        return None

    def _resolve_reference(self, ref: str) -> dict[str, Any] | None:
        """Resolve a $ref to get the actual schema definition"""
        # Check cache first
        if ref in self._definitions_cache:
            return self._definitions_cache[ref]

        # Parse the reference
        # References are like "#/definitions/io.k8s.api.core.v1.PersistentVolumeClaimStatus"
        if not ref.startswith("#/"):
            # External references not supported for now
            return None

        # Remove the leading '#/' and split the path
        ref_path = ref[2:].split("/")

        # Navigate the schema structure
        current = None
        if ref_path[0] == "definitions" and len(ref_path) > 1:
            definition_name = ref_path[1]
            if definition_name in self._definitions:
                current = self._definitions[definition_name]

                # Navigate any additional path segments
                for segment in ref_path[2:]:
                    if isinstance(current, dict) and segment in current:
                        current = current[segment]
                    else:
                        current = None
                        break

        # Cache the result
        if current is not None:
            self._definitions_cache[ref] = current
            return current

        # Fallback to the old method if definition not found
        if len(ref_path) > 1:
            definition_name = ref_path[-1]
            return self._get_status_schema_by_type(definition_name)

        return None

    def _get_status_schema_by_type(self, type_name: str) -> dict[str, Any]:
        """Get a status schema based on the type name"""
        # Extract the resource type from the definition name
        # e.g., "io.k8s.api.core.v1.PersistentVolumeClaimStatus" -> "PersistentVolumeClaim"
        if "Status" in type_name:
            resource_type = type_name.split(".")[-1].replace("Status", "")
            return self._get_default_status_schema_for_type(resource_type)

        return {"type": "object", "properties": {}}

    def _get_default_status_schema_for_type(self, resource_type: str) -> dict[str, Any]:
        """Get default status schema based on resource type patterns"""
        # Common patterns in Kubernetes status objects
        base_schema = {"type": "object", "properties": {}}

        # Add common status fields based on resource type
        if resource_type == "PersistentVolumeClaim":
            base_schema["properties"] = {
                "phase": {"type": "string", "enum": ["Pending", "Bound", "Lost"]},
                "accessModes": {
                    "type": "array",
                    "items": {"type": "string", "enum": ["ReadWriteOnce", "ReadOnlyMany", "ReadWriteMany"]},
                },
                "capacity": {"type": "object", "additionalProperties": {"type": "string"}},
                "conditions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "type": {"type": "string"},
                            "status": {"type": "string"},
                            "lastTransitionTime": {"type": "string"},
                            "reason": {"type": "string"},
                            "message": {"type": "string"},
                        },
                    },
                },
            }
        elif resource_type in ["StatefulSet", "DaemonSet", "ReplicaSet"]:
            base_schema["properties"] = {
                "replicas": {"type": "integer"},
                "readyReplicas": {"type": "integer"},
                "currentReplicas": {"type": "integer"},
                "updatedReplicas": {"type": "integer"},
                "observedGeneration": {"type": "integer"},
                "conditions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "type": {"type": "string"},
                            "status": {"type": "string", "enum": ["True", "False", "Unknown"]},
                            "lastTransitionTime": {"type": "string"},
                        },
                    },
                },
            }
        elif resource_type == "PersistentVolume":
            base_schema["properties"] = {
                "phase": {"type": "string", "enum": ["Pending", "Available", "Bound", "Released", "Failed"]},
                "message": {"type": "string"},
                "reason": {"type": "string"},
            }
        elif resource_type == "StorageClass":
            # StorageClass typically doesn't have status
            base_schema["properties"] = {}
        else:
            # Default status with conditions
            base_schema["properties"] = {
                "conditions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "type": {"type": "string"},
                            "status": {"type": "string", "enum": ["True", "False", "Unknown"]},
                            "lastTransitionTime": {"type": "string"},
                            "reason": {"type": "string"},
                            "message": {"type": "string"},
                        },
                    },
                },
                "observedGeneration": {"type": "integer"},
            }

            # Add phase for resources that commonly have it
            if resource_type in ["Job", "CronJob", "Backup", "Restore"]:
                properties = base_schema["properties"]
                if isinstance(properties, dict):
                    properties["phase"] = {
                        "type": "string",
                        "enum": ["Pending", "Running", "Succeeded", "Failed", "Unknown"],
                    }

        return base_schema

    def generate_status_from_schema(self, schema: dict[str, Any], resource_body: dict[str, Any]) -> dict[str, Any]:
        """Generate a realistic status based on the schema"""
        if not schema or schema.get("type") != "object":
            return {}

        status = {}
        properties = schema.get("properties", {})

        # Check if resource is configured as not ready
        is_ready = self._is_resource_ready(resource_body)

        for field_name, field_schema in properties.items():
            # Resolve any $ref in the field schema
            if "$ref" in field_schema:
                resolved_schema = self._resolve_reference(field_schema["$ref"])
                if resolved_schema:
                    field_schema = resolved_schema

            value = self._generate_value_for_field(field_name, field_schema, resource_body, is_ready)
            if value is not None:
                status[field_name] = value

        return status

    def _is_resource_ready(self, resource_body: dict[str, Any]) -> bool:
        """Check if resource should be generated as ready"""
        # Check annotations for test configuration
        metadata = resource_body.get("metadata", {})
        annotations = metadata.get("annotations", {})

        # Allow configuration via annotation "fake-client.io/ready"
        if annotations.get("fake-client.io/ready", "").lower() == "false":
            return False

        # Also check for a more specific ready status in spec
        if "readyStatus" in resource_body.get("spec", {}):
            return bool(resource_body["spec"]["readyStatus"])

        # Default to ready
        return True

    def _generate_value_for_field(
        self, field_name: str, field_schema: dict[str, Any], resource_body: dict[str, Any], is_ready: bool = True
    ) -> Any:
        """Generate a value for a specific field based on its schema"""
        field_type = field_schema.get("type", "string")

        if "enum" in field_schema:
            # For enums, pick an appropriate value
            return self._pick_enum_value(field_name, field_schema["enum"], is_ready)

        if field_type == "string":
            return self._generate_string_value(field_name, is_ready)
        elif field_type == "integer":
            return self._generate_integer_value(field_name, resource_body, is_ready)
        elif field_type == "boolean":
            return self._generate_boolean_value(field_name, is_ready)
        elif field_type == "array":
            return self._generate_array_value(field_name, field_schema, resource_body, is_ready)
        elif field_type == "object":
            return self._generate_object_value(field_name, field_schema, resource_body, is_ready)

        return None

    def _pick_enum_value(self, field_name: str, enum_values: list[str], is_ready: bool = True) -> str:
        """Pick an appropriate enum value based on field name"""
        if not enum_values:
            return ""

        # Smart selection based on field name and ready status
        if field_name == "phase":
            if is_ready:
                # Prefer positive states
                positive_states = ["Bound", "Running", "Active", "Ready", "Available", "Succeeded", "Complete"]
                for state in positive_states:
                    if state in enum_values:
                        return state
            else:
                # Prefer negative/pending states
                negative_states = ["Failed", "Error", "Terminating", "Pending", "Unknown"]
                for state in negative_states:
                    if state in enum_values:
                        return state
            # Fallback to first value
            return enum_values[0]

        elif field_name == "status" or field_name.endswith("Status"):
            # For condition statuses
            if is_ready and "True" in enum_values:
                return "True"
            elif not is_ready and "False" in enum_values:
                return "False"
            elif "Unknown" in enum_values:
                return "Unknown"

        elif field_name == "type" or field_name.endswith("Type"):
            # For condition types, prefer "Ready" or "Available"
            preferred = ["Ready", "Available", "Initialized", "Progressing"]
            for pref in preferred:
                if pref in enum_values:
                    return pref

        # Default to first value
        return enum_values[0]

    def _generate_string_value(self, field_name: str, is_ready: bool = True) -> str:
        """Generate a string value based on field name"""
        if "time" in field_name.lower() or "timestamp" in field_name.lower():
            return datetime.now(timezone.utc).isoformat()
        elif field_name == "message":
            return "Resource is ready" if is_ready else "Resource is not ready"
        elif field_name == "reason":
            return "ResourceReady" if is_ready else "ResourceNotReady"
        elif field_name.endswith("IP"):
            return f"10.0.0.{random.randint(1, 254)}"
        elif field_name == "hostname":
            return "node-1"
        elif field_name == "storagePolicyID":
            return "default-policy"
        else:
            return f"test-{field_name}"

    def _generate_integer_value(self, field_name: str, resource_body: dict[str, Any], is_ready: bool = True) -> int:
        """Generate an integer value based on field name"""
        if "replicas" in field_name:
            # Match the spec replicas if available
            spec_replicas = resource_body.get("spec", {}).get("replicas", 1)
            if is_ready:
                if field_name in ["replicas", "readyReplicas", "availableReplicas", "updatedReplicas"]:
                    return spec_replicas
                elif field_name == "unavailableReplicas":
                    return 0
            else:
                if field_name == "replicas":
                    return spec_replicas
                elif field_name in ["readyReplicas", "availableReplicas", "updatedReplicas"]:
                    return 0
                elif field_name == "unavailableReplicas":
                    return spec_replicas
        elif field_name == "observedGeneration":
            return resource_body.get("metadata", {}).get("generation", 1)
        elif field_name == "restartCount":
            return 0
        elif field_name.endswith("Count"):
            return 1
        else:
            return 1
        return 1

    def _generate_boolean_value(self, field_name: str, is_ready: bool = True) -> bool:
        """Generate a boolean value based on field name"""
        # Generally prefer positive values unless not ready
        negative_indicators = ["disabled", "failed", "error", "unavailable", "notready"]
        field_lower = field_name.lower()

        for indicator in negative_indicators:
            if indicator in field_lower:
                return False

        return is_ready

    def _generate_array_value(
        self, field_name: str, field_schema: dict[str, Any], resource_body: dict[str, Any], is_ready: bool = True
    ) -> list[Any]:
        """Generate an array value based on field schema"""
        items_schema = field_schema.get("items", {})

        # Resolve $ref in items if present
        if "$ref" in items_schema:
            resolved_items = self._resolve_reference(items_schema["$ref"])
            if resolved_items:
                items_schema = resolved_items

        if field_name == "conditions":
            # Generate standard conditions
            return self._generate_conditions(is_ready)
        elif field_name == "accessModes":
            # Use access modes from spec if available
            spec_modes = resource_body.get("spec", {}).get("accessModes", ["ReadWriteOnce"])
            return spec_modes
        elif field_name == "addresses":
            return [{"type": "InternalIP", "address": "10.0.0.1"}]
        elif field_name == "ports":
            return resource_body.get("spec", {}).get("ports", [{"port": 80}])
        else:
            # Generate a single item based on the items schema
            item = self._generate_value_for_field(f"{field_name}_item", items_schema, resource_body, is_ready)
            return [item] if item is not None else []

    def _generate_object_value(
        self, field_name: str, field_schema: dict[str, Any], resource_body: dict[str, Any], is_ready: bool = True
    ) -> dict[str, Any]:
        """Generate an object value based on field schema"""
        if field_name == "capacity":
            # For PVC capacity, match the requested storage
            requested = resource_body.get("spec", {}).get("resources", {}).get("requests", {})
            return requested.copy() if requested else {"storage": "1Gi"}
        elif field_name == "allocatedResources":
            # Match capacity
            return self._generate_object_value("capacity", field_schema, resource_body, is_ready)
        elif "properties" in field_schema:
            # Generate based on properties
            obj = {}
            for prop_name, prop_schema in field_schema["properties"].items():
                # Resolve any $ref in property schema
                if "$ref" in prop_schema:
                    resolved = self._resolve_reference(prop_schema["$ref"])
                    if resolved:
                        prop_schema = resolved

                value = self._generate_value_for_field(prop_name, prop_schema, resource_body, is_ready)
                if value is not None:
                    obj[prop_name] = value
            return obj
        elif "additionalProperties" in field_schema:
            # For maps like capacity, labels, etc.
            if field_name in ["capacity", "allocatedResources", "requests", "limits"]:
                return {"storage": "1Gi", "cpu": "100m", "memory": "128Mi"}
            else:
                return {"key1": "value1"}
        else:
            return {}

    def _generate_conditions(self, is_ready: bool = True) -> list[dict[str, Any]]:
        """Generate standard Kubernetes conditions"""
        if is_ready:
            return [
                {
                    "type": "Ready",
                    "status": "True",
                    "lastTransitionTime": datetime.now(timezone.utc).isoformat(),
                    "reason": "ResourceReady",
                    "message": "Resource is ready",
                },
                {
                    "type": "Available",
                    "status": "True",
                    "lastTransitionTime": datetime.now(timezone.utc).isoformat(),
                    "reason": "ResourceAvailable",
                    "message": "Resource is available",
                },
            ]
        else:
            return [
                {
                    "type": "Ready",
                    "status": "False",
                    "lastTransitionTime": datetime.now(timezone.utc).isoformat(),
                    "reason": "ResourceNotReady",
                    "message": "Resource is not ready",
                },
                {
                    "type": "Available",
                    "status": "False",
                    "lastTransitionTime": datetime.now(timezone.utc).isoformat(),
                    "reason": "ResourceUnavailable",
                    "message": "Resource is unavailable",
                },
            ]
