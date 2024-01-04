from ocp_resources.resource import NamespacedResource


class ControllerRevision(NamespacedResource):
    """
    https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/controller-revision-v1/
    """

    api_group = NamespacedResource.ApiGroup.APPS

    def __init__(
        self,
        owner_references=None,
        revision_object=None,
        revision=None,
        **kwargs,
    ):
        """
        Args:
            owner_references (list, optional): List of objects depended on this object.
            revision_object (object, optional): the Data Object representing the state.
            revision (int64): indicates the revision of the state represented by Data.
        """
        super().__init__(**kwargs)
        self.owner_references = owner_references
        self.revision_object = revision_object
        self.revision = revision

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file:
            if not self.revision:
                raise ValueError("Passing yaml_file or parameter 'revision' is required.")
            self.res.update({"revision": self.revision})

            if self.owner_references:
                self.res.setdefault("metadata", {}).update({"ownerReference": self.owner_references})
            if self.revision_object:
                self.res.update({"data": self.revision_object.res})
