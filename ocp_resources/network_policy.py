from ocp_resources.resource import NamespacedResource


class NetworkPolicy(NamespacedResource):
    """
    NetworkPolicy object.
    """

    api_group = NamespacedResource.ApiGroup.NETWORKING_K8S_IO
