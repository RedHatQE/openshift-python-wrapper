# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md

from typing import Any

from timeout_sampler import TimeoutSampler

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.resource import NamespacedResource
from ocp_resources.utils.constants import (
    DEFAULT_CLUSTER_RETRY_EXCEPTIONS,
    NOT_FOUND_ERROR_EXCEPTION_DICT,
    PROTOCOL_ERROR_EXCEPTION_DICT,
)


class VirtualMachineFileRestore(NamespacedResource):
    """
    VirtualMachineFileRestore is the Schema for the virtualmachinefilerestores API.
    """

    api_group: str = NamespacedResource.ApiGroup.FILERESTORE_KUBEVIRT_IO

    def __init__(
        self,
        source: dict[str, Any] | None = None,
        source_path: str | None = None,
        target: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            source (dict[str, Any]): Source specifies where to restore files from (PVC, VolumeSnapshot, or
              remote storage).

            source_path (str): SourcePath specifies the file or directory path to restore from the
              backup. If not specified, manual restore mode is enabled (volume
              is hotplugged but no automatic restore).

            target (dict[str, Any]): Target is a reference to the target VirtualMachine to restore files
              into.

        """
        super().__init__(**kwargs)

        self.source = source
        self.source_path = source_path
        self.target = target

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.source is None:
                raise MissingRequiredArgumentError(argument="self.source")

            if self.target is None:
                raise MissingRequiredArgumentError(argument="self.target")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["source"] = self.source
            _spec["target"] = self.target

            if self.source_path is not None:
                _spec["sourcePath"] = self.source_path

    # End of generated code

    class Phase:
        NEW: str = "New"
        INIT: str = "Init"
        HOTPLUGGING: str = "Hotplugging"
        WAITING_FOR_ATTACHMENT: str = "WaitingForAttachment"
        SSH_CONNECTING: str = "SSHConnecting"
        RESTORING: str = "Restoring"
        VOLUME_READY: str = "VolumeReady"
        CLEANUP: str = "Cleanup"
        SUCCEEDED: str = "Succeeded"
        FAILED: str = "Failed"

    def wait_for_phase(self, target_phase: str, timeout: int = 300, sleep: int = 5) -> None:
        """Wait for a restore phase, reporting an unexpected failure immediately.

        Transient API read failures are retried within the same timeout.

        Args:
            target_phase: Phase to wait for, including Failed when failure is expected.
            timeout: Maximum wait time in seconds.
            sleep: Polling interval in seconds.

        Raises:
            RuntimeError: If the restore fails before reaching the requested phase.
            TimeoutExpiredError: If the requested phase is not reached before the timeout.
        """
        self.logger.info(f"Waiting for {self.kind} '{self.name}' to reach phase '{target_phase}'")
        previous_phase = None
        for status in TimeoutSampler(
            wait_timeout=timeout,
            sleep=sleep,
            exceptions_dict=PROTOCOL_ERROR_EXCEPTION_DICT
            | NOT_FOUND_ERROR_EXCEPTION_DICT
            | DEFAULT_CLUSTER_RETRY_EXCEPTIONS,
            func=lambda: self.instance.get("status", {}),
        ):
            phase = status.get("phase")
            if phase != previous_phase:
                self.logger.info(f"{self.kind} '{self.name}' phase: {phase}")
                previous_phase = phase
            if phase == target_phase:
                return
            if phase == self.Phase.FAILED:
                error_message = status.get("errorMessage", "Unknown error")
                raise RuntimeError(f"{self.kind} '{self.name}' failed: {error_message}")

    @property
    def restored_files_count(self) -> int | None:
        """Number of restored files, or None before a transfer or in manual mode.

        A count of zero means an automatic transfer ran without copying any files.
        """
        return self.instance.get("status", {}).get("restoredFilesCount")

    @classmethod
    def from_snapshot(
        cls,
        target_vm_name: str,
        source_snapshot_name: str,
        source_path: str | None = None,
        source_namespace: str | None = None,
        **kwargs: Any,
    ) -> "VirtualMachineFileRestore":
        """Build a file restore from a VolumeSnapshot without creating it on the cluster.

        Args:
            target_vm_name: Name of the target VirtualMachine in the restore's namespace.
            source_snapshot_name: Name of the source VolumeSnapshot.
            source_path: Path to restore. Omit to enable manual restore mode.
            source_namespace: Namespace of the source snapshot. Omit to use the restore's namespace.
            **kwargs: Additional arguments passed to the generated constructor.

        Returns:
            A VirtualMachineFileRestore configured to restore from the snapshot.
        """
        snapshot: dict[str, str] = {"name": source_snapshot_name}
        if source_namespace is not None:
            snapshot["namespace"] = source_namespace

        return cls(
            source={"snapshot": snapshot},
            source_path=source_path,
            target={"apiGroup": cls.ApiGroup.KUBEVIRT_IO, "kind": "VirtualMachine", "name": target_vm_name},
            **kwargs,
        )

    @classmethod
    def from_pvc(
        cls,
        target_vm_name: str,
        source_pvc_name: str,
        source_path: str | None = None,
        source_namespace: str | None = None,
        **kwargs: Any,
    ) -> "VirtualMachineFileRestore":
        """Build a file restore from a PVC without creating it on the cluster.

        Args:
            target_vm_name: Name of the target VirtualMachine in the restore's namespace.
            source_pvc_name: Name of the source PersistentVolumeClaim.
            source_path: Path to restore. Omit to enable manual restore mode.
            source_namespace: Namespace of the source PVC. Omit to use the restore's namespace.
            **kwargs: Additional arguments passed to the generated constructor.

        Returns:
            A VirtualMachineFileRestore configured to restore from the PVC.
        """
        pvc: dict[str, str] = {"name": source_pvc_name}
        if source_namespace is not None:
            pvc["namespace"] = source_namespace

        return cls(
            source={"pvc": pvc},
            source_path=source_path,
            target={"apiGroup": cls.ApiGroup.KUBEVIRT_IO, "kind": "VirtualMachine", "name": target_vm_name},
            **kwargs,
        )
