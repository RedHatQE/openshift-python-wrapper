from ocp_resources.resource import NamespacedResource


class VirtualMachineInstanceReplicaSet(NamespacedResource):
    """
    VirtualMachineInstancePreset object.
    """

    api_group = NamespacedResource.ApiGroup.KUBEVIRT_IO
