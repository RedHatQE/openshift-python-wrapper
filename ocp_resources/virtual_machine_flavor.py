from ocp_resources.resource import NamespacedResource


class VirtualMachineFlavor(NamespacedResource):
    api_group = NamespacedResource.ApiGroup.FLAVOR_KUBEVIRT_IO
