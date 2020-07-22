from .resource import NamespacedResource


class NetworkPolicy(NamespacedResource):
    """
    NetworkPolicy object.
    """

    api_group = "networking.k8s.io"
