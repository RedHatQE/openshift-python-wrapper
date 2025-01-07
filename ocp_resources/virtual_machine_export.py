# -*- coding: utf-8 -*-

from ocp_resources.utils.constants import TIMEOUT_1MINUTE
from ocp_resources.persistent_volume_claim import PersistentVolumeClaim
from ocp_resources.resource import MissingRequiredArgumentError, NamespacedResource
from ocp_resources.virtual_machine import VirtualMachine
from ocp_resources.virtual_machine_snapshot import VirtualMachineSnapshot


class VirtualMachineExport(NamespacedResource):
    """
    VirtualMachineExport object.
    """

    api_group: str = NamespacedResource.ApiGroup.EXPORT_KUBEVIRT_IO

    class SourceKind:
        VM = VirtualMachine.kind
        VM_SNAPSHOT = VirtualMachineSnapshot.kind
        PVC = PersistentVolumeClaim.kind

    def __init__(
        self,
        source_api_group: str | None = None,
        source_kind: str | None = None,
        source_name: str | None = None,
        token_secret_ref: str | None = None,
        ttl_duration: str | None = None,
        delete_timeout: int = TIMEOUT_1MINUTE,
        **kwargs,
    ) -> None:
        """
        Args:
            source_api_group (str): Api group of the exported resource
            source_kind (str): Kind of the exported resource
            source_name (str): Name of the exported resource inside the same namespace

            token_secret_ref (str): TokenSecretRef is the name of the custom-defined secret that contains
              the token used by the export server pod

            ttl_duration (str): ttlDuration limits the lifetime of an export If this field is set,
              after this duration has passed from counting from
              CreationTimestamp, the export is eligible to be automatically
              deleted. If this field is omitted, a reasonable default is
              applied.
        """
        super().__init__(
            delete_timeout=delete_timeout,
            **kwargs,
        )
        self.source_api_group = source_api_group
        self.source_kind = source_kind
        self.source_name = source_name
        self.token_secret_ref = token_secret_ref
        self.ttl_duration = ttl_duration

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if not (self.source_kind and self.source_name):
                raise MissingRequiredArgumentError(argument="'source_kind' and 'source_name'")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["source"] = {
                "apiGroup": self.source_api_group,
                "kind": self.source_kind,
                "name": self.source_name,
            }

            if self.token_secret_ref:
                _spec["tokenSecretRef"] = self.token_secret_ref

            if self.ttl_duration:
                _spec["ttlDuration"] = self.ttl_duration
