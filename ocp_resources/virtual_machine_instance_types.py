from ocp_resources.resource import NamespacedResource


class VirtualMachineInstancetype(NamespacedResource):
    api_group = NamespacedResource.ApiGroup.INSTANCETYPE_KUBEVIRT_IO
