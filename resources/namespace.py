import logging

from resources.utils import NudgeTimers, nudge_delete

from .resource import Resource


LOGGER = logging.getLogger(__name__)

_DELETE_NUDGE_DELAY = 30
_DELETE_NUDGE_INTERVAL = 5


class Namespace(Resource):
    """
    Namespace object, inherited from Resource.
    """

    api_version = "v1"

    class Status(Resource.Status):
        ACTIVE = "Active"

    def __init__(
        self, name, client=None, teardown=True, label=None,
    ):
        super().__init__(name=name, client=client, teardown=teardown)
        self.label = label

    def to_dict(self):
        res = super().to_dict()
        if self.label:
            res.setdefault("metadata", {}).setdefault("labels", {}).update(self.label)
        return res

    # TODO: remove the nudge when the underlying issue with namespaces stuck in
    # Terminating state is fixed.
    # Upstream bug: https://github.com/kubernetes/kubernetes/issues/60807
    def nudge_delete(self):
        timers = NudgeTimers()
        nudge_delete(name=self.name, timers=timers)
