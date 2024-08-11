from warnings import warn
from ocp_resources.virtual_machine_instancetype import VirtualMachineInstancetype  # noqa: F401

warn(
    f"The module {__name__} is deprecated and will be removed in version 4.17, `VirtualMachineInstancetype` should be imported from `ocp_resources.virtual_machine_instancetype`",
    DeprecationWarning,
    stacklevel=2,
)
