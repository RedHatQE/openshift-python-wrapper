import time

from openshift.dynamic.exceptions import ConflictError

from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.resource import Resource
from ocp_resources.utils import TimeoutSampler


SLEEP = 1


class NodeNetworkState(Resource):
    api_group = Resource.ApiGroup.NMSTATE_IO

    def __init__(
        self,
        name=None,
        client=None,
        teardown=True,
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
        status = self.instance.to_dict()["status"]
        self.desired_state = status.get("desiredState", {"interfaces": []})

    def set_interface(self, interface):

        # First drop the interface is's already in the list
        interfaces = [
            iface
            for iface in self.desired_state["interfaces"]
            if iface["name"] != interface["name"]
        ]

        # Add the interface
        interfaces.append(interface)
        self.desired_state["interfaces"] = interfaces

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file:
            self.res.update(
                {
                    "spec": {
                        "nodeName": self.name,
                        "managed": True,
                        "desiredState": self.desired_state,
                    }
                }
            )

    def apply(self):
        retries_on_conflict = 3
        while True:
            try:
                self.res["metadata"] = self.instance.to_dict()["metadata"]
                self.update(self.res)
                break
            except ConflictError as e:
                retries_on_conflict -= 1
                if retries_on_conflict == 0:
                    raise e
                time.sleep(1)

    def wait_until_up(self, name):
        def _find_up_interface():
            iface = self.get_interface(name=name)
            if iface.get("state") == self.Interface.State.UP:
                return iface

            return None

        self.logger.info(f"Checking if interface {name} is up -- {self.name}")
        samples = TimeoutSampler(
            wait_timeout=TIMEOUT_4MINUTES, sleep=SLEEP, func=_find_up_interface
        )
        for sample in samples:
            if sample:
                return

    def wait_until_deleted(self, name):
        self.logger.info(f"Checking if interface {name} is deleted -- {self.name}")
        samples = TimeoutSampler(
            wait_timeout=self.delete_timeout,
            sleep=SLEEP,
            func=self.get_interface,
            name=name,
        )
        for sample in samples:
            if not sample:
                return

    @property
    def interfaces(self):
        return self.instance.to_dict()["status"]["currentState"]["interfaces"]

    @property
    def routes(self):
        return self.instance.status.currentState.routes

    def ipv4(self, iface):
        for interface in self.interfaces:
            if interface["name"] == iface:
                addresses = interface["ipv4"]["address"]
                if addresses:
                    return interface["ipv4"]["address"][0]["ip"]

    def get_interface(self, name):
        for interface in self.interfaces:
            if interface["name"] == name:
                return interface
        return {}
