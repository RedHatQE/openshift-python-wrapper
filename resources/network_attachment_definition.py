from .resource import NamespacedResource


class NetworkAttachmentDefinition(NamespacedResource):
    """
    NetworkAttachmentDefinition object.
    """

    api_group = "k8s.cni.cncf.io"
    resource_name = None

    def wait_for_status(
        self, status, timeout=None, label_selector=None, resource_version=None
    ):
        raise NotImplementedError(f"{self.kind} does not have status")

    def to_dict(self):
        res = super().to_dict()
        if self.resource_name is not None:
            res["metadata"]["annotations"] = {
                "k8s.v1.cni.cncf.io/resourceName": self.resource_name
            }
        res["spec"] = {}
        return res
