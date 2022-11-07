# -*- coding: utf-8 -*-

from ocp_resources.constants import TIMEOUT_1MINUTE
from ocp_resources.persistent_volume_claim import PersistentVolumeClaim
from ocp_resources.resource import NamespacedResource
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
        if not (source_kind and source_name and token_secret_ref) and not yaml_file:
            raise ValueError(
                "source_kind, source_name and token_secret_ref or a yaml_file is required"
            )

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

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file:
            self.res.update(
                {
                    "spec": {
                        "tokenSecretRef": self.token_secret_ref,
                        "source": {
                            "apiGroup": self.source_api_group,
                            "kind": self.source_kind,
                            "name": self.source_name,
                        },
                    }
                }
            )
