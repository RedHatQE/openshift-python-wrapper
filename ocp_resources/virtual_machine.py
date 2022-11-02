# -*- coding: utf-8 -*-


import xmltodict
from openshift.dynamic.exceptions import ResourceNotFoundError
from urllib3.exceptions import ProtocolError

from ocp_resources.node import Node
from ocp_resources.pod import Pod
from ocp_resources.resource import TIMEOUT, NamespacedResource
from ocp_resources.utils import TimeoutExpiredError, TimeoutSampler


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

    def __init__(
        self,
        name,
        namespace,
        client=None,
        body=None,
        teardown=True,
        privileged_client=None,
    ):
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            teardown=teardown,
            privileged_client=privileged_client,
        )
        self.body = body

    @property
    def _subresource_api_url(self):
        return (
            f"{self.client.configuration.host}/"
            f"apis/subresources.kubevirt.io/{self.api().api_version}/"
            f"namespaces/{self.namespace}/virtualmachines/{self.name}"
        )

    def api_request(self, method, action, **params):
        return super().api_request(
            method=method, action=action, url=self._subresource_api_url, **params
        )

    def to_dict(self):
        res = super().to_dict()
        body_spec = self.body.get("spec") if self.body else None
        res["spec"] = body_spec or {"template": {"spec": {}}}
        return res

    def start(self, timeout=TIMEOUT, wait=False):
        self.api_request(method="PUT", action="start")
        if wait:
            return self.wait_for_status(timeout=timeout, status=True)

    def restart(self, timeout=TIMEOUT, wait=False):
        self.api_request(method="PUT", action="restart")
        if wait:
            self.vmi.virt_launcher_pod.wait_deleted()
            return self.vmi.wait_until_running(timeout=timeout, stop_status="dummy")

    def stop(self, timeout=TIMEOUT, wait=False):
        self.api_request(method="PUT", action="stop")
        if wait:
            self.wait_for_status(timeout=timeout, status=None)
            return self.vmi.wait_deleted()

    def wait_for_status(self, status, timeout=TIMEOUT, sleep=1):
        """
        Wait for resource to be in status

        Args:
            status: Expected status: True for a running VM, None for a stopped VM.
            timeout (int): Time to wait for the resource.

        Raises:
            TimeoutExpiredError: If timeout reached.
        """
        self.logger.info(
            f"Wait for {self.kind} {self.name} status to be {'ready' if status == True else status}"
        )
        samples = TimeoutSampler(
            wait_timeout=timeout,
            sleep=sleep,
            exceptions=ProtocolError,
            func=self.api().get,
            field_selector=f"metadata.name=={self.name}",
            namespace=self.namespace,
        )
        for sample in samples:
            if sample.items:
                # VM with runStrategy does not have spec.running attribute
                # VM status should be taken from spec.status.ready
                if self.ready == status:
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
        return self.instance.status["ready"] if self.instance.status else None


class VirtualMachineInstance(NamespacedResource):
    """
    Virtual Machine Instance object, inherited from Resource.
    """

    api_group = NamespacedResource.ApiGroup.KUBEVIRT_IO

    class Status(NamespacedResource.Status):
        RUNNING = "Running"
        SCHEDULING = "Scheduling"

    def __init__(self, name, namespace, client=None, privileged_client=None):
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            privileged_client=privileged_client,
        )

    @property
    def _subresource_api_url(self):
        return (
            f"{self.client.configuration.host}/"
            f"apis/subresources.kubevirt.io/{self.api().api_version}/"
            f"namespaces/{self.namespace}/virtualmachineinstances/{self.name}"
        )

    def api_request(self, method, action, **params):
        return super().api_request(
            method=method, action=action, url=self._subresource_api_url, **params
        )

    def to_dict(self):
        res = super().to_dict()
        return res

    def pause(self, timeout=TIMEOUT, wait=False):
        self.api_request(method="PUT", action="pause")
        if wait:
            return self.wait_for_pause_status(pause=True, timeout=timeout)

    def unpause(self, timeout=TIMEOUT, wait=False):
        self.api_request(method="PUT", action="unpause")
        if wait:
            return self.wait_for_pause_status(pause=False, timeout=timeout)

    @property
    def interfaces(self):
        return self.instance.status.interfaces

    @property
    def virt_launcher_pod(self):
        pods = list(
            Pod.get(
                dyn_client=self.privileged_client or self.client,
                namespace=self.namespace,
                label_selector=f"kubevirt.io=virt-launcher,kubevirt.io/created-by={self.instance.metadata.uid}",
            )
        )
        migration_state = self.instance.status.migrationState
        if migration_state:
            #  After VM migration there are two pods, one in Completed status and one in Running status.
            #  We need to return the Pod that is not in Completed status.
            for pod in pods:
                if migration_state.targetPod == pod.name:
                    return pod
        else:
            return pods[0]

        raise ResourceNotFoundError

    @property
    def virt_handler_pod(self):
        pods = list(
            Pod.get(
                dyn_client=self.privileged_client or self.client,
                label_selector="kubevirt.io=virt-handler",
            )
        )
        for pod in pods:
            if pod.instance["spec"]["nodeName"] == self.instance.status.nodeName:
                return pod

        raise ResourceNotFoundError

    def wait_until_running(self, timeout=TIMEOUT, logs=True, stop_status=None):
        """
        Wait until VMI is running

        Args:
            timeout (int): Time to wait for VMI.
            logs (bool): True to extract logs from the VMI pod and from the VMI.
            stop_status (str): Status which should stop the wait and failed.

        Raises:
            TimeoutExpiredError: If VMI failed to run.
        """
        try:
            self.wait_for_status(
                status=self.Status.RUNNING, timeout=timeout, stop_status=stop_status
            )
        except TimeoutExpiredError:
            if not logs:
                raise

            virt_pod = self.virt_launcher_pod
            if virt_pod:
                self.logger.debug(f"{virt_pod.name} *****LOGS*****")
                self.logger.debug(virt_pod.log(container="compute"))

            raise

    def wait_for_pause_status(self, pause, timeout=TIMEOUT):
        """
        Wait for Virtual Machine Instance to be paused / unpaused.
        Paused status is checked in libvirt and in the VMI conditions.

        Args:
            pause (bool): True for paused, False for unpause
            timeout (int): Time to wait for the resource.

        Raises:
            TimeoutExpiredError: If resource not exists.
        """
        self.logger.info(
            f"Wait until {self.kind} {self.name} is "
            f"{'Paused' if pause else 'Unpuased'}"
        )
        self.wait_for_domstate_pause_status(pause=pause, timeout=timeout)
        self.wait_for_vmi_condition_pause_status(pause=pause, timeout=timeout)

    def wait_for_domstate_pause_status(self, pause, timeout=TIMEOUT):
        pause_status = "paused" if pause else "running"
        samples = TimeoutSampler(
            wait_timeout=timeout,
            sleep=1,
            exceptions=(ProtocolError),
            func=self.get_domstate,
        )
        for sample in samples:
            if pause_status in sample:
                return

    def wait_for_vmi_condition_pause_status(self, pause, timeout=TIMEOUT):
        samples = TimeoutSampler(
            wait_timeout=timeout,
            sleep=1,
            exceptions=(ProtocolError),
            func=self.get_vmi_active_condition,
        )
        for sample in samples:
            # VM in state change
            # We have commanded a [un]pause condition via the API but the CR has not been updated yet to match.
            # 'reason' may not exist yet
            # or
            # 'reason' may still exist after unpause if the CR has not been updated before we perform this check
            if (pause and not sample.get("reason")) or (
                sample.get("reason") == "PausedByUser" and not pause
            ):
                continue
            # Paused VM
            if pause and sample["reason"] == "PausedByUser":
                return
            # Unpaused VM
            if not (pause and sample.get("reason")):
                return

    @property
    def node(self):
        """
        Get the node name where the VM is running

        Returns:
            Node: Node
        """
        return Node(
            client=self.privileged_client or self.client,
            name=self.instance.status.nodeName,
        )

    def get_xml(self):
        """
        Get virtual machine instance XML

        Returns:
            xml_output(string): VMI XML in the multi-line string
        """
        return self.virt_launcher_pod.execute(
            command=["virsh", "dumpxml", f"{self.namespace}_{self.name}"],
            container="compute",
        )

    def get_domstate(self):
        """
        Get virtual machine instance Status.

        Current workaround, as VM/VMI shows no status/phase == Paused yet.
        Bug: https://bugzilla.redhat.com/show_bug.cgi?id=1805178

        Returns:
            String: VMI Status as string
        """
        return self.virt_launcher_pod.execute(
            command=["virsh", "domstate", f"{self.namespace}_{self.name}"],
            container="compute",
        )

    def get_vmi_active_condition(self):
        """A VMI may have multiple conditions; the active one it the one with
        'lastTransitionTime'"""
        return {
            k: v
            for condition in self.instance.status.conditions
            for k, v in condition.items()
            if condition["lastTransitionTime"]
        }

    @property
    def xml_dict(self):
        """Get virtual machine instance XML as dict"""

        return xmltodict.parse(xml_input=self.get_xml(), process_namespaces=True)

    @property
    def guest_os_info(self):
        return self.api_request(method="GET", action="guestosinfo")

    @property
    def guest_fs_info(self):
        return self.api_request(method="GET", action="filesystemlist")

    @property
    def guest_user_info(self):
        return self.api_request(method="GET", action="userlist")

    @property
    def os_version(self):
        vmi_os_version = self.instance.status.guestOSInfo.get("version", {})
        if not vmi_os_version:
            self.logger.warning(
                "Guest agent is not installed on the VM; OS version is not available."
            )
        return vmi_os_version

    def interface_ip(self, interface):
        iface_ip = [
            iface["ipAddress"]
            for iface in self.interfaces
            if iface["interfaceName"] == interface
        ]
        return iface_ip[0] if iface_ip else None


class VirtualMachineInstanceMigration(NamespacedResource):
    api_group = NamespacedResource.ApiGroup.KUBEVIRT_IO

    def __init__(self, name, namespace, vmi=None, client=None, teardown=True):
        super().__init__(
            name=name, namespace=namespace, client=client, teardown=teardown
        )
        self._vmi = vmi

    def to_dict(self):
        # When creating VirtualMachineInstanceMigration vmi is mandatory but when calling get()
        # we cannot pass vmi.
        assert self._vmi, "vmi is mandatory for create"

        res = super().to_dict()
        res["spec"] = {"vmiName": self._vmi.name}
        return res


class VirtualMachineInstancePreset(NamespacedResource):
    """
    VirtualMachineInstancePreset object.
    """

    api_group = NamespacedResource.ApiGroup.KUBEVIRT_IO

    def __init__(
        self,
        name,
        namespace,
        client=None,
        teardown=True,
    ):
        super().__init__(
            name=name, namespace=namespace, client=client, teardown=teardown
        )


class VirtualMachineInstanceReplicaSet(NamespacedResource):
    """
    VirtualMachineInstancePreset object.
    """

    api_group = NamespacedResource.ApiGroup.KUBEVIRT_IO

    def __init__(
        self,
        name,
        namespace,
        client=None,
        teardown=True,
    ):
        super().__init__(
            name=name, namespace=namespace, client=client, teardown=teardown
        )
