"""Test fixtures for schema validation testing."""

# Simple pod schema for testing
SIMPLE_POD_SCHEMA = {
    "type": "object",
    "required": ["apiVersion", "kind", "metadata", "spec"],
    "properties": {
        "apiVersion": {"type": "string", "enum": ["v1"]},
        "kind": {"type": "string", "enum": ["Pod"]},
        "metadata": {
            "type": "object",
            "required": ["name"],
            "properties": {
                "name": {"type": "string", "minLength": 1, "maxLength": 253},
                "namespace": {"type": "string", "minLength": 1, "maxLength": 253},
                "labels": {"type": "object", "additionalProperties": {"type": "string"}},
            },
        },
        "spec": {
            "type": "object",
            "required": ["containers"],
            "properties": {
                "containers": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "type": "object",
                        "required": ["name", "image"],
                        "properties": {
                            "name": {"type": "string", "minLength": 1},
                            "image": {"type": "string", "minLength": 1},
                            "ports": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "containerPort": {"type": "integer", "minimum": 1, "maximum": 65535},
                                        "protocol": {"type": "string", "enum": ["TCP", "UDP", "SCTP"]},
                                    },
                                },
                            },
                        },
                    },
                }
            },
        },
    },
}

# Simple ConfigMap schema
SIMPLE_CONFIGMAP_SCHEMA = {
    "type": "object",
    "required": ["apiVersion", "kind", "metadata"],
    "properties": {
        "apiVersion": {"type": "string", "enum": ["v1"]},
        "kind": {"type": "string", "enum": ["ConfigMap"]},
        "metadata": {
            "type": "object",
            "required": ["name"],
            "properties": {
                "name": {"type": "string", "minLength": 1, "maxLength": 253},
                "namespace": {"type": "string", "minLength": 1, "maxLength": 253},
            },
        },
        "data": {"type": "object", "additionalProperties": {"type": "string"}},
        "binaryData": {"type": "object", "additionalProperties": {"type": "string", "format": "byte"}},
    },
}

# Schema with nested references for testing
DEPLOYMENT_SCHEMA = {
    "type": "object",
    "required": ["apiVersion", "kind", "metadata"],
    "properties": {
        "apiVersion": {"type": "string", "enum": ["apps/v1"]},
        "kind": {"type": "string", "enum": ["Deployment"]},
        "metadata": {
            "type": "object",
            "required": ["name"],
            "properties": {"name": {"type": "string", "minLength": 1, "maxLength": 253}},
        },
        "spec": {
            "type": "object",
            "properties": {
                "replicas": {"type": "integer", "minimum": 0, "default": 1},
                "selector": {
                    "type": "object",
                    "required": ["matchLabels"],
                    "properties": {"matchLabels": {"type": "object", "additionalProperties": {"type": "string"}}},
                },
                "template": {
                    "type": "object",
                    "properties": {
                        "metadata": {
                            "type": "object",
                            "properties": {"labels": {"type": "object", "additionalProperties": {"type": "string"}}},
                        },
                        "spec": {
                            "type": "object",
                            "required": ["containers"],
                            "properties": {"containers": {"type": "array", "minItems": 1}},
                        },
                    },
                },
            },
        },
    },
}

# Invalid schema for error testing
INVALID_SCHEMA = {
    "type": "invalid_type",  # Invalid type
    "properties": "should_be_object",  # Invalid properties format
}

# Valid pod resource
VALID_POD = {
    "apiVersion": "v1",
    "kind": "Pod",
    "metadata": {"name": "test-pod", "namespace": "default"},
    "spec": {"containers": [{"name": "nginx", "image": "nginx:latest"}]},
}

# Invalid pod - missing required field
INVALID_POD_MISSING_NAME = {
    "apiVersion": "v1",
    "kind": "Pod",
    "metadata": {
        "namespace": "default"
        # Missing 'name'
    },
    "spec": {"containers": [{"name": "nginx", "image": "nginx:latest"}]},
}

# Invalid pod - wrong type
INVALID_POD_WRONG_TYPE = {
    "apiVersion": "v1",
    "kind": "Pod",
    "metadata": {"name": "test-pod", "namespace": "default"},
    "spec": {
        "containers": "should-be-array"  # Wrong type
    },
}

# Invalid pod - enum violation
INVALID_POD_WRONG_ENUM = {
    "apiVersion": "v2",  # Wrong API version
    "kind": "Pod",
    "metadata": {"name": "test-pod"},
    "spec": {"containers": [{"name": "nginx", "image": "nginx:latest"}]},
}

# Invalid pod - port out of range
INVALID_POD_PORT_RANGE = {
    "apiVersion": "v1",
    "kind": "Pod",
    "metadata": {"name": "test-pod"},
    "spec": {
        "containers": [
            {
                "name": "nginx",
                "image": "nginx:latest",
                "ports": [
                    {
                        "containerPort": 70000  # Out of range
                    }
                ],
            }
        ]
    },
}
