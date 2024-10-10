class MissingRequiredArgumentError(Exception):
    def __init__(self, argument: str) -> None:
        self.argument = argument

    def __repr__(self) -> str:
        return f"Missing required argument/s. Either provide yaml_file, kind_dict or pass {self.argument}"


class MissingResourceResError(Exception):
    def __repr__(self) -> str:
        return "Failed to generate resource self.res"


class MissingTemplateVariables(Exception):
    def __init__(self, var, template):
        self.var = var
        self.template = template

    def __str__(self):
        return f"Missing variables {self.var} for template {self.template}"


class ExecOnPodError(Exception):
    def __init__(self, command, rc, out, err):
        self.cmd = command
        self.rc = rc
        self.out = out
        self.err = err

    def __str__(self):
        return "Command execution failure: " f"{self.cmd}, " f"RC: {self.rc}, " f"OUT: {self.out}, " f"ERR: {self.err}"


class NNCPConfigurationFailed(Exception):
    pass
