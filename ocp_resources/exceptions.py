from typing import Any
from warnings import warn


class MissingRequiredArgumentError(Exception):
    def __init__(self, argument: str) -> None:
        self.argument = argument

    def __str__(self) -> str:
        return f"Missing required argument/s. Either provide yaml_file, kind_dict or pass {self.argument}"


class MissingResourceError(Exception):
    def __init__(self, name: str) -> None:
        self.resource_name = name

    def __str__(self) -> str:
        return f"Failed to generate resource: {self.resource_name}"


class MissingResourceResError(Exception):
    def __init__(self, name: str) -> None:
        warn(
            "MissingResourceResError is deprecated and will be removed in the future. Use MissingResourceError instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        self.resource_name = name

    def __str__(self) -> str:
        return f"Failed to generate resource: {self.resource_name}"


class MissingTemplateVariables(Exception):
    def __init__(self, var: str, template: str) -> None:
        self.var = var
        self.template = template

    def __str__(self):
        return f"Missing variables {self.var} for template {self.template}"


class ExecOnPodError(Exception):
    def __init__(self, command: list[str], rc: int, out: str, err: Any) -> None:
        self.cmd = command
        self.rc = rc
        self.out = out
        self.err = err

    def __str__(self):
        return f"Command execution failure: {self.cmd}, RC: {self.rc}, OUT: {self.out}, ERR: {self.err}"


class NNCPConfigurationFailed(Exception):
    pass


class ResourceTeardownError(Exception):
    def __init__(self, resource: Any):
        self.resource = resource

    def __str__(self):
        return f"Failed to execute teardown for resource {self.resource}"


class ClientWithBasicAuthError(Exception):
    pass


class ValidationError(Exception):
    """Raised when resource validation against OpenAPI schema fails."""

    def __init__(self, message: str, path: str = "", schema_error: Any = None) -> None:
        """
        Initialize ValidationError.

        Args:
            message: Human-readable error message
            path: JSONPath to the invalid field (e.g., "spec.containers[0].image")
            schema_error: Original jsonschema validation error for debugging
        """
        self.message = message
        self.path = path
        self.schema_error = schema_error
        super().__init__(message)

    def __str__(self) -> str:
        if self.path:
            return f"Validation error at '{self.path}': {self.message}"
        return f"Validation error: {self.message}"
