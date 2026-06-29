# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.resource import NamespacedResource


class VirtualMachineBackup(NamespacedResource):
    """
    VirtualMachineBackup defines the operation of backing up a VM
    """

    api_group: str = NamespacedResource.ApiGroup.BACKUP_KUBEVIRT_IO

    def __init__(
        self,
        force_full_backup: bool | None = None,
        mode: str | None = None,
        pvc_name: str | None = None,
        skip_quiesce: bool | None = None,
        source: dict[str, Any] | None = None,
        token_secret_ref: str | None = None,
        ttl_duration: str | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            force_full_backup (bool): ForceFullBackup indicates that a full backup is desired

            mode (str): Mode specifies the way the backup output will be recieved

            pvc_name (str): PvcName required in push mode. Specifies the name of the PVC where the
              backup output will be stored

            skip_quiesce (bool): SkipQuiesce indicates whether the VM's filesystem shoule not be
              quiesced before the backup

            source (dict[str, Any]): Source specifies the backup source - either a VirtualMachine or a
              VirtualMachineBackupTracker. When Kind is VirtualMachine: performs
              a backup of the specified VM. When Kind is
              VirtualMachineBackupTracker: uses the tracker to get the source VM
              and the base checkpoint for incremental backup. The tracker will
              be updated with the new checkpoint after backup completion.

            token_secret_ref (str): TokenSecretRef is the name of the secret that will be used to pull the
              backup from an associated endpoint

            ttl_duration (str): TtlDuration limits the lifetime of a pull mode backup and its export
              If this field is set, after this duration has passed from counting
              from CreationTimestamp, the backup is eligible to be automatically
              considered as complete. If this field is omitted, a reasonable
              default is applied.

        """
        super().__init__(**kwargs)

        self.force_full_backup = force_full_backup
        self.mode = mode
        self.pvc_name = pvc_name
        self.skip_quiesce = skip_quiesce
        self.source = source
        self.token_secret_ref = token_secret_ref
        self.ttl_duration = ttl_duration

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.source is None:
                raise MissingRequiredArgumentError(argument="self.source")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["source"] = self.source

            if self.force_full_backup is not None:
                _spec["forceFullBackup"] = self.force_full_backup

            if self.mode is not None:
                _spec["mode"] = self.mode

            if self.pvc_name is not None:
                _spec["pvcName"] = self.pvc_name

            if self.skip_quiesce is not None:
                _spec["skipQuiesce"] = self.skip_quiesce

            if self.token_secret_ref is not None:
                _spec["tokenSecretRef"] = self.token_secret_ref

            if self.ttl_duration is not None:
                _spec["ttlDuration"] = self.ttl_duration

    # End of generated code

    class Mode:
        PUSH: str = "Push"
        PULL: str = "Pull"
