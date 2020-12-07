# -*- coding: utf-8 -*-

from .resource import Resource


class PersistentVolume(Resource):
    """
    PersistentVolume object
    """

    api_version = Resource.ApiVersion.V1

    def __init__(
        self, name, client=None, teardown=True,
    ):
        super().__init__(name=name, client=client, teardown=teardown)

    @property
    def max_available_pvs(self):
        """
        Returns the maximum number (int) of PV's which are in 'Available' state
        """
        return len(
            [pv for pv in self.api().get()["items"] if pv.status.phase == "Available"]
        )
