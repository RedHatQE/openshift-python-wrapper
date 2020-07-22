import logging
import time

from openshift.dynamic.exceptions import ConflictError
from resources.utils import TimeoutSampler

from .resource import Resource


LOGGER = logging.getLogger(__name__)

SLEEP = 1
TIMEOUT = 120


class NodeNetworkState(Resource):

    api_group = "nmstate.io"

    def __init__(self, name, teardown=True):
        super().__init__(name=name, teardown=teardown)
        status = self.instance.to_dict()["status"]
        if "desiredState" in status:
            self.desired_state = status["desiredState"]
        else:
            self.desired_state = {"interfaces": []}

    def set_interface(self, interface):

        # First drop the interface is's already in the list
        interfaces = [
            i
            for i in self.desired_state["interfaces"]
            if not (i["name"] == interface["name"])
        ]

        # Add the interface
        interfaces.append(interface)
        self.desired_state["interfaces"] = interfaces

    def to_dict(self):
        res = super()._base_body()
        res.update(
            {
                "spec": {
                    "nodeName": self.name,
                    "managed": True,
                    "desiredState": self.desired_state,
                }
            }
        )
        return res

    def apply(self):
        resource = self.to_dict()
        retries_on_conflict = 3
        while True:
            try:
                resource["metadata"] = self.instance.to_dict()["metadata"]
                self.update(resource)
                break
            except ConflictError as e:
                retries_on_conflict -= 1
                if retries_on_conflict == 0:
                    raise e
                time.sleep(1)

    def wait_until_up(self, name):
        def _find_up_interface():
            for interface in self.interfaces:
                if interface["name"] == name and interface["state"] == "up":
                    return interface
            return None

        LOGGER.info(f"Checking if interface {name} is up -- {self.name}")
        samples = TimeoutSampler(timeout=TIMEOUT, sleep=SLEEP, func=_find_up_interface)
        for sample in samples:
            if sample:
                return

    def wait_until_deleted(self, name):
        def _find_deleted_interface():
            for interface in self.interfaces:
                if interface["name"] == name:
                    return interface
            return None

        LOGGER.info(f"Checking if interface {name} is deleted -- {self.name}")
        samples = TimeoutSampler(
            timeout=TIMEOUT, sleep=SLEEP, func=_find_deleted_interface
        )
        for sample in samples:
            if not sample:
                return

    @property
    def interfaces(self):
        return self.instance.status.currentState.interfaces

    @property
    def routes(self):
        return self.instance.status.currentState.routes

    def ipv4(self, iface):
        for interface in self.interfaces:
            if interface["name"] == iface:
                addresses = interface["ipv4"]["address"]
                if addresses:
                    return interface["ipv4"]["address"][0]["ip"]
