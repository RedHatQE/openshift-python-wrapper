# -*- coding: utf-8 -*-


from openshift.dynamic.exceptions import ResourceNotFoundError

from ocp_resources.constants import PROTOCOL_ERROR_EXCEPTION_DICT, TIMEOUT_4MINUTES
from ocp_resources.resource import TIMEOUT, NamespacedResource
from ocp_resources.utils import TimeoutSampler
from ocp_resources.virtual_machine import VirtualMachine


class VirtualMachineSnapshot(NamespacedResource):
    """
    VirtualMachineSnapshot object.
    """

    api_group = NamespacedResource.ApiGroup.SNAPSHOT_KUBEVIRT_IO

    def __init__(
        self,
        name=None,
        namespace=None,
        vm_name=None,
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

    def to_dict(self):
        res = super().to_dict()
        if self.yaml_file:
            return res

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
        self.logger.info(
            f"Wait for {self.kind} {self.name} status to be {'' if status else 'not '}ready to use"
        )

        samples = TimeoutSampler(
            wait_timeout=timeout,
            sleep=1,
            exceptions_dict=PROTOCOL_ERROR_EXCEPTION_DICT,
            func=lambda: self.instance.get("status", {}).get("readyToUse") == status,
        )
        for sample in samples:
            if sample:
                return

    def wait_snapshot_done(self, timeout=TIMEOUT_4MINUTES):
        """
        Wait for the the snapshot to be done. This check 2 parameters, the snapshot status to be readyToUse
        and the VM status snapshotInProgress to be None.

        Args:
            timeout (int): Time to wait.

        Raises:
            TimeoutExpiredError: If timeout reached.
        """
        self.wait_ready_to_use(timeout=timeout)

        vm = VirtualMachine(
            client=self.client,
            namespace=self.namespace,
            name=self.vm_name,
        )

        if vm.exists:
            return vm.wait_for_status_none(status="snapshotInProgress", timeout=timeout)
        raise ResourceNotFoundError(f"VirtualMachine: {vm.name} not found")
