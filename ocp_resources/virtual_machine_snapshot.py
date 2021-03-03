# -*- coding: utf-8 -*-

import logging

from urllib3.exceptions import ProtocolError

from ocp_resources.resource import TIMEOUT, NamespacedResource
from ocp_resources.utils import TimeoutSampler
from ocp_resources.virtual_machine import VirtualMachine


LOGGER = logging.getLogger(__name__)


class VirtualMachineSnapshot(NamespacedResource):
    """
    VirtualMachineSnapshot object.
    """

    api_group = NamespacedResource.ApiGroup.SNAPSHOT_KUBEVIRT_IO

    def __init__(self, name, namespace, vm_name, client=None, teardown=True):
        super().__init__(
            name=name, namespace=namespace, client=client, teardown=teardown
        )
        self.vm_name = vm_name

    def to_dict(self):
        res = super().to_dict()
        spec = res.setdefault("spec", {})
        spec.setdefault("source", {})[
            "apiGroup"
        ] = NamespacedResource.ApiGroup.KUBEVIRT_IO
        spec["source"]["kind"] = VirtualMachine.kind
        spec["source"]["name"] = self.vm_name
        return res

    def wait_ready_to_use(self, status=True, timeout=TIMEOUT):
        """
        Wait for VirtualMachineSnapshot to be in readyToUse status

        Args:
            status: Expected status: True for a ready to use VirtualMachineSnapshot, False otherwise.
            timeout (int): Time to wait for the resource.

        Raises:
            TimeoutExpiredError: If timeout reached.
        """
        LOGGER.info(
            f"Wait for {self.kind} {self.name} status to be {'' if status else 'not '}ready to use"
        )

        samples = TimeoutSampler(
            wait_timeout=timeout,
            sleep=1,
            exceptions=ProtocolError,
            func=lambda: self.instance.get("status", {}).get("readyToUse", None)
            == status,
        )
        for sample in samples:
            if sample:
                return
