from ocp_resources.resource import NamespacedResource


class VirtualMachineInstancetype(NamespacedResource):
    api_group = NamespacedResource.ApiGroup.INSTANCE_TYPE_KUBEVIRT_IO
