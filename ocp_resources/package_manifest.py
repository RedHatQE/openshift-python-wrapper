from ocp_resources.resource import NamespacedResource


class PackageManifest(NamespacedResource):
    api_group = NamespacedResource.ApiGroup.PACKAGES_OPERATORS_COREOS_COM
