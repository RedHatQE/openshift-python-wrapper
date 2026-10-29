# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md


from typing import Any

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.resource import NamespacedResource


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
