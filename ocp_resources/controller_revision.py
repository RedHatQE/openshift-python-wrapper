from ocp_resources.resource import NamespacedResource


class ControllerRevision(NamespacedResource):
    """
    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.26/#controllerrevision-v1-apps
    """

    api_group = NamespacedResource.ApiGroup.APPS

    def __init__(
        self,
        owner_references=None,
        revision_object=None,
        **kwargs,
    ):
        """
        Args:
            owner_references (list): List of objects depended by this object.
            revision_object (int): indicates the revision of the state represented by Data.
        """
        super().__init__(**kwargs)
        self.owner_references = owner_references
        self.revision_object = revision_object

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file:
            if self.owner_references:
                self.res.setdefault("metadata", {}).update(
                    {"ownerReference": self.owner_references}
                )
            if self.revision_object:
                self.res.update({"data": self.revision_object.res})
