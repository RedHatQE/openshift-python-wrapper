from ocp_resources.resource import NamespacedResource


class SSP(NamespacedResource):
    """
    SSP object.
    """

    api_group = NamespacedResource.ApiGroup.SSP_KUBEVIRT_IO
