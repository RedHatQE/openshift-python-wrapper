"""Test fixtures for resource validation."""

# Sample OpenAPI schema for Pod (simplified)
POD_SCHEMA = {
    "type": "object",
    "properties": {
        "apiVersion": {"type": "string"},
        "kind": {"type": "string"},
        "metadata": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "namespace": {"type": "string"},
            },
            "required": ["name"],
        },
        "spec": {
            "type": "object",
            "properties": {
                "containers": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "image": {"type": "string"},
                        },
                        "required": ["name", "image"],
                    },
                },
            },
            "required": ["containers"],
        },
    },
    "required": ["apiVersion", "kind", "metadata", "spec"],
}

# Valid Pod resource dict
POD_VALID = {
    "apiVersion": "v1",
    "kind": "Pod",
    "metadata": {
        "name": "test-pod",
        "namespace": "default",
    },
    "spec": {
        "containers": [
            {
                "name": "nginx",
                "image": "nginx:latest",
            }
        ],
    },
}

# Pod missing required containers field
POD_MISSING_REQUIRED = {
    "apiVersion": "v1",
    "kind": "Pod",
    "metadata": {
        "name": "test-pod",
        "namespace": "default",
    },
    "spec": {},  # Missing required 'containers' field
}

# Pod with invalid container name (not a string)
POD_INVALID_CONTAINER_NAME = {
    "apiVersion": "v1",
    "kind": "Pod",
    "metadata": {
        "name": "test-pod",
        "namespace": "default",
    },
    "spec": {
        "containers": [
            {
                "name": 123,  # Should be string
                "image": "nginx:latest",
            }
        ],
    },
}

# Pod with invalid image (missing required field)
POD_INVALID_IMAGE = {
    "apiVersion": "v1",
    "kind": "Pod",
    "metadata": {
        "name": "test-pod",
        "namespace": "default",
    },
    "spec": {
        "containers": [
            {
                "name": "nginx",
                # Missing required 'image' field
            }
        ],
    },
}

# Sample OpenAPI schema for Deployment (simplified)
