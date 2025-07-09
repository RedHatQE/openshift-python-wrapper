"""Status schema parser for generating dynamic status from resource schemas"""

import random
from datetime import datetime, timezone
from typing import Any, Union


class StatusSchemaParser:
    """Parser for generating status from resource schemas"""

    def __init__(self, resource_mappings: dict[str, Any]) -> None:
        self.resource_mappings = resource_mappings
        self._definitions_cache: dict[str, Any] = {}

    def get_status_schema_for_resource(self, kind: str, api_version: str) -> Union[dict[str, Any], None]:
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

    def _resolve_reference(self, ref: str) -> Union[dict[str, Any], None]:
        """Resolve a $ref to get the actual schema definition"""
        # For now, return a placeholder - in real implementation would follow the ref
        # References are like "#/definitions/io.k8s.api.core.v1.PersistentVolumeClaimStatus"
        ref_parts = ref.split("/")
        if len(ref_parts) > 2 and ref_parts[-1]:
            definition_name = ref_parts[-1]

            # Try to find the definition in our mappings
            # This is simplified - real implementation would load from schema files
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

        for field_name, field_schema in properties.items():
            value = self._generate_value_for_field(field_name, field_schema, resource_body)
            if value is not None:
                status[field_name] = value

        return status

    def _generate_value_for_field(
        self, field_name: str, field_schema: dict[str, Any], resource_body: dict[str, Any]
    ) -> Any:
        """Generate a value for a specific field based on its schema"""
        field_type = field_schema.get("type", "string")

        if "enum" in field_schema:
            # For enums, pick an appropriate value
            return self._pick_enum_value(field_name, field_schema["enum"])

        if field_type == "string":
            return self._generate_string_value(field_name)
        elif field_type == "integer":
            return self._generate_integer_value(field_name, resource_body)
        elif field_type == "boolean":
            return self._generate_boolean_value(field_name)
        elif field_type == "array":
            return self._generate_array_value(field_name, field_schema, resource_body)
        elif field_type == "object":
            return self._generate_object_value(field_name, field_schema, resource_body)

        return None

    def _pick_enum_value(self, field_name: str, enum_values: list[str]) -> str:
        """Pick an appropriate enum value based on field name"""
        if not enum_values:
            return ""

        # Smart selection based on field name
        if field_name == "phase":
            # Prefer positive states
            positive_states = ["Bound", "Running", "Active", "Ready", "Available", "Succeeded", "Complete"]
            for state in positive_states:
                if state in enum_values:
                    return state
            # Fallback to first non-negative state
            negative_states = ["Failed", "Error", "Terminating", "Unknown", "Pending"]
            for value in enum_values:
                if value not in negative_states:
                    return value

        elif field_name == "status" or field_name.endswith("Status"):
            # For condition statuses, prefer "True"
            if "True" in enum_values:
                return "True"
            elif "Active" in enum_values:
                return "Active"

        elif field_name == "type" or field_name.endswith("Type"):
            # For condition types, prefer "Ready" or "Available"
            preferred = ["Ready", "Available", "Initialized", "Progressing"]
            for pref in preferred:
                if pref in enum_values:
                    return pref

        # Default to first value
        return enum_values[0]

    def _generate_string_value(self, field_name: str) -> str:
        """Generate a string value based on field name"""
        if "time" in field_name.lower() or "timestamp" in field_name.lower():
            return datetime.now(timezone.utc).isoformat()
        elif field_name == "message":
            return "Resource is ready"
        elif field_name == "reason":
            return "ResourceReady"
        elif field_name.endswith("IP"):
            return f"10.0.0.{random.randint(1, 254)}"
        elif field_name == "hostname":
            return "node-1"
        elif field_name == "storagePolicyID":
            return "default-policy"
        else:
            return f"test-{field_name}"

    def _generate_integer_value(self, field_name: str, resource_body: dict[str, Any]) -> int:
        """Generate an integer value based on field name"""
        if "replicas" in field_name:
            # Match the spec replicas if available
            spec_replicas = resource_body.get("spec", {}).get("replicas", 1)
            if field_name in ["replicas", "readyReplicas", "availableReplicas", "updatedReplicas"]:
                return spec_replicas
            elif field_name == "unavailableReplicas":
                return 0
        elif field_name == "observedGeneration":
            return resource_body.get("metadata", {}).get("generation", 1)
        elif field_name == "restartCount":
            return 0
        elif field_name.endswith("Count"):
            return 1
        else:
            return 1
        return 1

    def _generate_boolean_value(self, field_name: str) -> bool:
        """Generate a boolean value based on field name"""
        # Generally prefer positive values
        negative_indicators = ["disabled", "failed", "error", "unavailable", "notready"]
        field_lower = field_name.lower()

        for indicator in negative_indicators:
            if indicator in field_lower:
                return False

        return True

    def _generate_array_value(
        self, field_name: str, field_schema: dict[str, Any], resource_body: dict[str, Any]
    ) -> list[Any]:
        """Generate an array value based on field schema"""
        items_schema = field_schema.get("items", {})

        if field_name == "conditions":
            # Generate standard conditions
            return self._generate_conditions()
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
            item = self._generate_value_for_field(f"{field_name}_item", items_schema, resource_body)
            return [item] if item is not None else []

    def _generate_object_value(
        self, field_name: str, field_schema: dict[str, Any], resource_body: dict[str, Any]
    ) -> dict[str, Any]:
        """Generate an object value based on field schema"""
        if field_name == "capacity":
            # For PVC capacity, match the requested storage
            requested = resource_body.get("spec", {}).get("resources", {}).get("requests", {})
            return requested.copy() if requested else {"storage": "1Gi"}
        elif field_name == "allocatedResources":
            # Match capacity
            return self._generate_object_value("capacity", field_schema, resource_body)
        elif "properties" in field_schema:
            # Generate based on properties
            obj = {}
            for prop_name, prop_schema in field_schema["properties"].items():
                value = self._generate_value_for_field(prop_name, prop_schema, resource_body)
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

    def _generate_conditions(self) -> list[dict[str, Any]]:
        """Generate standard Kubernetes conditions"""
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
