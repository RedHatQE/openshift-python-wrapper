from ocp_resources.resource import NamespacedResource


class VirtualMachineInstancePreset(NamespacedResource):
    """
    VirtualMachineInstancePreset object.
    """

    api_group = NamespacedResource.ApiGroup.KUBEVIRT_IO

    def __init__(
        self,
        name=None,
        namespace=None,
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
