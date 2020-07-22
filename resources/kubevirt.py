from .resource import NamespacedResource


class KubeVirt(NamespacedResource):
    api_group = "kubevirt.io"
