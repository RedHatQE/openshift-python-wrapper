from ocp_resources.resource import NamespacedResource


class VirtualMachineClusterPreference(NamespacedResource):
    api_group = NamespacedResource.ApiGroup.INSTANCE_TYPE_KUBEVIRT_IO
