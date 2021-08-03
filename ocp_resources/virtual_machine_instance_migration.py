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
    ):
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            teardown=teardown,
            yaml_file=yaml_file,
        )
        self._vmi = vmi

    def to_dict(self):
        # When creating VirtualMachineInstanceMigration vmi is mandatory but when calling get()
        # we cannot pass vmi.
        res = super().to_dict()
        if self.yaml_file:
            return res

        assert self._vmi, "vmi is mandatory for create"
        res["spec"] = {"vmiName": self._vmi.name}
        return res
