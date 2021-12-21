from ocp_resources.resource import NamespacedResource


class VirtualMachineInstancePreset(NamespacedResource):
    """
    VirtualMachineInstancePreset object.
    """

    api_group = NamespacedResource.ApiGroup.KUBEVIRT_IO
