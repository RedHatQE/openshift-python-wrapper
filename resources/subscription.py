from .resource import NamespacedResource


class Subscription(NamespacedResource):
    api_group = "operators.coreos.com"
