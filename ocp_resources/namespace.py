import logging

from ocp_resources.resource import Resource
from ocp_resources.utils import TimeoutExpiredError, nudge_delete


LOGGER = logging.getLogger(__name__)

_DELETE_NUDGE_DELAY = 30
_DELETE_NUDGE_INTERVAL = 5


class Namespace(Resource):
    """
    Namespace object, inherited from Resource.
    """

    api_version = Resource.ApiVersion.V1

    class Status(Resource.Status):
        ACTIVE = "Active"

    def __init__(
        self,
        name,
        client=None,
        teardown=True,
        label=None,
    ):
        super().__init__(name=name, client=client, teardown=teardown)
        self.label = label

    def to_dict(self):
        res = super().to_dict()
        if self.label:
            res.setdefault("metadata", {}).setdefault("labels", {}).update(self.label)
        return res

    def client_wait_deleted(self, timeout):
        """
        client-side Wait until resource is deleted

        Args:
            timeout (int): Time to wait for the resource.

        """
        try:
            super().client_wait_deleted(timeout=timeout)
        except TimeoutExpiredError:
            nudge_delete(name=self.name)
