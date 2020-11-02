# -*- coding: utf-8 -*-

import logging

from resources.utils import TimeoutSampler
from resources.virtual_machine import VirtualMachine
from urllib3.exceptions import ProtocolError

from .resource import TIMEOUT, NamespacedResource


LOGGER = logging.getLogger(__name__)


class VirtualMachineSnapshot(NamespacedResource):
    """
    VirtualMachineSnapshot object.
    """

    api_group = NamespacedResource.ApiGroup.SNAPSHOT_KUBEVIRT_IO

    def __init__(self, name, namespace, vm_name, teardown=True):
        super().__init__(name=name, namespace=namespace, teardown=teardown)
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
            timeout=timeout,
            sleep=1,
            exceptions=ProtocolError,
            func=self.api().get,
            field_selector=f"metadata.name=={self.name}",
            namespace=self.namespace,
        )
        for sample in samples:
            if sample.items:
                if self.instance.get("status", {}).get("readyToUse", None) == status:
                    return
