# https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/controller-revision-v1/
from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.resource import NamespacedResource


class ControllerRevision(NamespacedResource):
    api_group = NamespacedResource.ApiGroup.APPS

    def __init__(
        self,
        name=None,
        namespace=None,
        client=None,
        teardown=True,
        timeout=TIMEOUT_4MINUTES,
        privileged_client=None,
        yaml_file=None,
        delete_timeout=TIMEOUT_4MINUTES,
        owner_references=None,
        revision_object=None,
        **kwargs,
    ):
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            teardown=teardown,
            timeout=timeout,
            privileged_client=privileged_client,
            yaml_file=yaml_file,
            delete_timeout=delete_timeout,
            **kwargs,
        )
        self.owner_references = owner_references
        self.revision_object = revision_object

    def to_dict(self):
        """
        Generate intended dict representation of the resource.
        """
        self._base_body()
        self.res["metadata"]["ownerReference"] = self.owner_references
        self.res["data"] = self.revision_object.res
