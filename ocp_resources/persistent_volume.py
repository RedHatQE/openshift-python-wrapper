# -*- coding: utf-8 -*-

from ocp_resources.resource import Resource


class PersistentVolume(Resource):
    """
    PersistentVolume object
    """

    api_version = Resource.ApiVersion.V1

    class Status(Resource.Status):
        RELEASED = "Released"

    @property
    def max_available_pvs(self):
        """
        Returns the maximum number (int) of PV's which are in 'Available' state
        """
        return len(
            [
                pv
                for pv in self.api.get()["items"]
                if pv.status.phase == Resource.Condition.AVAILABLE
            ]
        )
