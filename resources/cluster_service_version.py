from resources.resource import NamespacedResource


class ClusterServiceVersion(NamespacedResource):
    api_group = "operators.coreos.com"

    class Status(NamespacedResource.Status):
        INSTALLING = "Installing"
