from ocp_resources.resource import Resource


class Group(Resource):
    api_group = Resource.ApiGroup.USER_OPENSHIFT_IO

    def __init__(
        self,
        users=None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.users = users

    def to_dict(self) -> None:
        super().to_dict()
        if (not self.yaml_file) and self.users:
            self.res["users"] = self.users
