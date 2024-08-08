from warnings import warn
from ocp_resources.virtual_machine_instance_replica_set import VirtualMachineInstanceReplicaSet  # noqa: F401

warn(
    f"The module {__name__} is deprecated and will be removed in version 4.17, `VirtualMachineInstanceReplicaSet` should be imported from `ocp_resources.virtual_machine_instance_replica_set`",
    DeprecationWarning,
    stacklevel=2,
)
