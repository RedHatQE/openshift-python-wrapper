from ocp_resources.resource import NamespacedResource


class NetworkAttachmentDefinition(NamespacedResource):
    """
    NetworkAttachmentDefinition object.
    """

    api_group = NamespacedResource.ApiGroup.K8S_CNI_CNCF_IO
    resource_name = None

    def wait_for_status(
        self, status, timeout=None, label_selector=None, resource_version=None
    ):
        raise NotImplementedError(f"{self.kind} does not have status")

    def to_dict(self):
        res = super().to_dict()
        if self.yaml_file:
            return res

        if self.resource_name is not None:
            res["metadata"]["annotations"] = {
                f"{NamespacedResource.ApiGroup.K8S_V1_CNI_CNCF_IO}/resourceName": self.resource_name
            }
        res["spec"] = {}
        return res
