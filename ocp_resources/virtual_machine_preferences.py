from ocp_resources.resource import NamespacedResource


class VirtualMachinePreference(NamespacedResource):
    api_group = NamespacedResource.ApiGroup.INSTANCETYPE_KUBEVIRT_IO
