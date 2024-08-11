from warnings import warn
from ocp_resources.virtual_machine_cluster_preference import VirtualMachineClusterPreference  # noqa: F401

warn(
    f"The module {__name__} is deprecated and will be removed in version 4.17, `VirtualMachineClusterPreference` should be imported from `ocp_resources.virtual_machine_cluster_preference`",
    DeprecationWarning,
    stacklevel=2,
)
