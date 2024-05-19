from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.resource import NamespacedResource


class VirtualMachineInstanceMigration(NamespacedResource):
    api_group = NamespacedResource.ApiGroup.KUBEVIRT_IO

    def __init__(
        self,
        name=None,
        namespace=None,
        vmi=None,
        client=None,
        teardown=True,
        yaml_file=None,
        delete_timeout=TIMEOUT_4MINUTES,
        **kwargs,
    ):
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            teardown=teardown,
            yaml_file=yaml_file,
            delete_timeout=delete_timeout,
            **kwargs,
        )
        self._vmi = vmi

    def to_dict(self) -> None:
        # When creating VirtualMachineInstanceMigration vmi is mandatory but when calling get()
        # we cannot pass vmi.
        super().to_dict()
        if not self.yaml_file:
            assert self._vmi, "vmi is mandatory for create"
            self.res["spec"] = {"vmiName": self._vmi.name}
