from warnings import warn
from ocp_resources.virtual_machine_cluster_instancetype import VirtualMachineClusterInstancetype  # noqa: F401

warn(
    f"The module {__name__} is deprecated and will be removed in version 4.17, `VirtualMachineClusterInstancetype` should be imported from `ocp_resources.virtual_machine_cluster_instancetype`",
    DeprecationWarning,
    stacklevel=2,
)
