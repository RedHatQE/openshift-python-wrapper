from ocp_resources.constants import TIMEOUT_4MINUTES
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
        delete_timeout=TIMEOUT_4MINUTES,
        **kwargs,
    ):
        super().__init__(
            name=name,
            client=client,
            teardown=teardown,
            yaml_file=yaml_file,
            delete_timeout=delete_timeout,
            **kwargs,
        )
        self.label = label

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file and self.label:
            self.res.setdefault("metadata", {}).setdefault("labels", {}).update(
                self.label
            )
