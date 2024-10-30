from typing import Any


class MissingRequiredArgumentError(Exception):
    def __init__(self, argument: str) -> None:
        self.argument = argument

    def __str__(self) -> str:
        return f"Missing required argument/s. Either provide yaml_file, kind_dict or pass {self.argument}"


class MissingResourceResError(Exception):
    def __init__(self, name: str) -> None:
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
