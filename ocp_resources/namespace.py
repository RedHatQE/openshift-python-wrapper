from ocp_resources.resource import Resource


class Namespace(Resource):
    """
    Namespace object, inherited from Resource.
    """

    api_version = Resource.ApiVersion.V1

    class Status(Resource.Status):
        ACTIVE = "Active"

    def __init__(
        self,
        name=None,
        client=None,
        teardown=True,
        label=None,
        yaml_file=None,
    ):
        super().__init__(
            name=name, client=client, teardown=teardown, yaml_file=yaml_file
        )
        self.label = label

    def to_dict(self):
        res = super().to_dict()
        if self.yaml_file:
            return res

        if self.label:
            res.setdefault("metadata", {}).setdefault("labels", {}).update(self.label)
        return res
