# -*- coding: utf-8 -*-

from ocp_resources.constants import TIMEOUT_1MINUTE
from ocp_resources.persistent_volume_claim import PersistentVolumeClaim
from ocp_resources.resource import MissingRequiredArgumentError, NamespacedResource
from ocp_resources.virtual_machine import VirtualMachine
from ocp_resources.virtual_machine_snapshot import VirtualMachineSnapshot


class VirtualMachineExport(NamespacedResource):
    """
    VirtualMachineExport object.
    """

    api_group = NamespacedResource.ApiGroup.EXPORT_KUBEVIRT_IO

    class SourceKind:
        VM = VirtualMachine.kind
        VM_SNAPSHOT = VirtualMachineSnapshot.kind
        PVC = PersistentVolumeClaim.kind

    def __init__(
        self,
        name=None,
        namespace=None,
        client=None,
        teardown=True,
        token_secret_ref=None,
        source_api_group=None,
        source_kind=None,
        source_name=None,
        timeout=TIMEOUT_1MINUTE,
        delete_timeout=TIMEOUT_1MINUTE,
        yaml_file=None,
        **kwargs,
    ):
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            teardown=teardown,
            yaml_file=yaml_file,
            timeout=timeout,
            delete_timeout=delete_timeout,
            **kwargs,
        )
        self.token_secret_ref = token_secret_ref
        self.source_api_group = source_api_group
        self.source_kind = source_kind
        self.source_name = source_name

    def to_dict(self) -> None:
        super().to_dict()
        if not self.kind_dict and not self.yaml_file:
            if not (self.source_kind and self.source_name):
                raise MissingRequiredArgumentError(argument="'source_kind' and 'source_name'")
            self.res.update({
                "spec": {
                    "tokenSecretRef": self.token_secret_ref,
                    "source": {
                        "apiGroup": self.source_api_group,
                        "kind": self.source_kind,
                        "name": self.source_name,
                    },
                }
            })
