from .resource import NamespacedResource


class PackageManifest(NamespacedResource):
    api_group = "packages.operators.coreos.com"
