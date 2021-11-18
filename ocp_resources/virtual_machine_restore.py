# -*- coding: utf-8 -*-


import logging

from ocp_resources.constants import PROTOCOL_ERROR_EXCEPTION_DICT
from ocp_resources.resource import TIMEOUT, NamespacedResource
from ocp_resources.utils import TimeoutSampler
from ocp_resources.virtual_machine import VirtualMachine


LOGGER = logging.getLogger(__name__)


class VirtualMachineRestore(NamespacedResource):
    """
    VirtualMachineRestore object.
    """

    api_group = NamespacedResource.ApiGroup.SNAPSHOT_KUBEVIRT_IO

    def __init__(
        self,
        name=None,
        namespace=None,
        vm_name=None,
        snapshot_name=None,
        client=None,
        teardown=True,
        yaml_file=None,
    ):
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            teardown=teardown,
            yaml_file=yaml_file,
        )
        self.vm_name = vm_name
        self.snapshot_name = snapshot_name

    def to_dict(self):
        res = super().to_dict()
        if self.yaml_file:
            return res

        spec = res.setdefault("spec", {})
        spec.setdefault("target", {})[
            "apiGroup"
        ] = NamespacedResource.ApiGroup.KUBEVIRT_IO
        spec["target"]["kind"] = VirtualMachine.kind
        spec["target"]["name"] = self.vm_name
        spec["virtualMachineSnapshotName"] = self.snapshot_name
        return res

    def wait_complete(self, status=True, timeout=TIMEOUT):
        """
        Wait for VirtualMachineRestore to be in status complete

        Args:
            status: Expected status: True for a completed restore operation, False otherwise.
            timeout (int): Time to wait.

        Raises:
            TimeoutExpiredError: If timeout reached.
        """
        LOGGER.info(
            f"Wait for {self.kind} {self.name} status to be complete = {status}"
        )

        samples = TimeoutSampler(
            wait_timeout=timeout,
            sleep=1,
            exceptions_dict=PROTOCOL_ERROR_EXCEPTION_DICT,
            func=lambda: self.instance.get("status", {}).get("complete", None)
            == status,
        )
        for sample in samples:
            if sample:
                return
