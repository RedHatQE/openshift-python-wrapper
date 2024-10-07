# -*- coding: utf-8 -*-


from ocp_resources.constants import (
    DEFAULT_CLUSTER_RETRY_EXCEPTIONS,
    PROTOCOL_ERROR_EXCEPTION_DICT,
    TIMEOUT_4MINUTES,
)
from ocp_resources.resource import NamespacedResource
from timeout_sampler import TimeoutSampler
from ocp_resources.virtual_machine_instance import VirtualMachineInstance


class VirtualMachine(NamespacedResource):
    """
    Virtual Machine object, inherited from Resource.
    Implements actions start / stop / status / wait for VM status / is running
    """

    api_group = NamespacedResource.ApiGroup.KUBEVIRT_IO

    class RunStrategy:
        MANUAL = "Manual"
        HALTED = "Halted"
        ALWAYS = "Always"
        RERUNONFAILURE = "RerunOnFailure"

    class Status(NamespacedResource.Status):
        MIGRATING = "Migrating"
        PAUSED = "Paused"
        PROVISIONING = "Provisioning"
        STARTING = "Starting"
        STOPPED = "Stopped"
        STOPPING = "Stopping"
        WAITING_FOR_VOLUME_BINDING = "WaitingForVolumeBinding"
        ERROR_UNSCHEDULABLE = "ErrorUnschedulable"
        DATAVOLUME_ERROR = "DataVolumeError"
        ERROR_PVC_NOT_FOUND = "ErrorPvcNotFound"
        IMAGE_PULL_BACK_OFF = "ImagePullBackOff"
        ERR_IMAGE_PULL = "ErrImagePull"
        CRASH_LOOPBACK_OFF = "CrashLoopBackOff"

    def __init__(
        self,
        name=None,
        namespace=None,
        client=None,
        body=None,
        teardown=True,
        privileged_client=None,
        yaml_file=None,
        delete_timeout=TIMEOUT_4MINUTES,
        **kwargs,
    ):
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            teardown=teardown,
            privileged_client=privileged_client,
            yaml_file=yaml_file,
            delete_timeout=delete_timeout,
            **kwargs,
        )
        self.body = body

    @property
    def _subresource_api_url(self):
        return (
            f"{self.client.configuration.host}/"
            f"apis/subresources.kubevirt.io/{self.api.api_version}/"
            f"namespaces/{self.namespace}/virtualmachines/{self.name}"
        )

    def api_request(self, method, action, **params):
        return super().api_request(method=method, action=action, url=self._subresource_api_url, **params)

    def to_dict(self) -> None:
        super().to_dict()
        if not self.kind_dict and not self.yaml_file:
            body_spec = self.body.get("spec") if self.body else None
            self.res["spec"] = body_spec or {"template": {"spec": {}}}

    def start(self, timeout=TIMEOUT_4MINUTES, wait=False):
        self.api_request(method="PUT", action="start")
        if wait:
            return self.wait_for_ready_status(timeout=timeout, status=True)

    def restart(self, timeout=TIMEOUT_4MINUTES, wait=False):
        self.api_request(method="PUT", action="restart")
        if wait:
            self.vmi.virt_launcher_pod.wait_deleted()
            return self.vmi.wait_until_running(timeout=timeout, stop_status="dummy")

    def stop(self, timeout=TIMEOUT_4MINUTES, vmi_delete_timeout=TIMEOUT_4MINUTES, wait=False):
        self.api_request(method="PUT", action="stop")
        if wait:
            self.wait_for_ready_status(timeout=timeout, status=None)
            return self.vmi.wait_deleted(timeout=vmi_delete_timeout)

    def wait_for_ready_status(self, status, timeout=TIMEOUT_4MINUTES, sleep=1):
        """
        Wait for VM resource ready status to be at desire status

        Args:
            status (any): True for a running VM, None for a stopped VM.
            timeout (int): Time to wait for the resource.

        Raises:
            TimeoutExpiredError: If timeout reached.
        """
        self.logger.info(f"Wait for {self.kind} {self.name} status to be {'ready' if status is True else status}")
        samples = TimeoutSampler(
            wait_timeout=timeout,
            sleep=sleep,
            exceptions_dict={
                **PROTOCOL_ERROR_EXCEPTION_DICT,
                **DEFAULT_CLUSTER_RETRY_EXCEPTIONS,
            },
            func=self.api.get,
            field_selector=f"metadata.name=={self.name}",
            namespace=self.namespace,
        )
        for sample in samples:
            if sample.items and self.ready == status:
                # VM with runStrategy does not have spec.running attribute
                # VM status should be taken from spec.status.ready
                return

    def get_interfaces(self):
        return self.instance.spec.template.spec.domain.devices.interfaces

    @property
    def vmi(self):
        """
        Get VMI

        Returns:
            VirtualMachineInstance: VMI
        """
        return VirtualMachineInstance(
            client=self.client,
            name=self.name,
            namespace=self.namespace,
            privileged_client=self.privileged_client or self.client,
        )

    @property
    def ready(self):
        """
        Get VM status

        Returns:
            True if Running else None
        """
        return self.instance.get("status", {}).get("ready")

    @property
    def printable_status(self):
        """
        Get VM printableStatus

        Returns:
            VM printableStatus if VM.status.printableStatus else None
        """
        return self.instance.get("status", {}).get("printableStatus")

    def wait_for_status_none(self, status, timeout=TIMEOUT_4MINUTES):
        self.logger.info(f"Wait for {self.kind} {self.name} status {status} to be None")
        for sample in TimeoutSampler(
            wait_timeout=timeout,
            sleep=1,
            exceptions_dict=PROTOCOL_ERROR_EXCEPTION_DICT,
            func=lambda: self.instance.get("status", {}).get(status),
        ):
            if sample is None:
                return
