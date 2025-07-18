import shlex
from typing import Any

import xmltodict
from kubernetes.dynamic.exceptions import ResourceNotFoundError
from timeout_sampler import TimeoutExpiredError, TimeoutSampler

from ocp_resources.node import Node
from ocp_resources.pod import Pod
from ocp_resources.resource import NamespacedResource
from ocp_resources.utils.constants import PROTOCOL_ERROR_EXCEPTION_DICT, TIMEOUT_4MINUTES, TIMEOUT_5SEC, TIMEOUT_30SEC


class VirtualMachineInstance(NamespacedResource):
    """
    Virtual Machine Instance object, inherited from Resource.
    """

    api_group = NamespacedResource.ApiGroup.KUBEVIRT_IO

    class Status(NamespacedResource.Status):
        SCHEDULING = "Scheduling"
        SCHEDULED = "Scheduled"

    def __init__(
        self,
        name=None,
        namespace=None,
        client=None,
        yaml_file=None,
        delete_timeout=TIMEOUT_4MINUTES,
        **kwargs,
    ):
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            yaml_file=yaml_file,
            delete_timeout=delete_timeout,
            **kwargs,
        )

    @property
    def _subresource_api_url(self):
        return (
            f"{self.client.configuration.host}/"
            f"apis/subresources.kubevirt.io/{self.api.api_version}/"
            f"namespaces/{self.namespace}/virtualmachineinstances/{self.name}"
        )

    def api_request(
        self, method: str, action: str, url: str = "", retry_params: dict[str, int] | None = None, **params: Any
    ) -> dict[str, Any]:
        default_vmi_api_request_retry_params: dict[str, int] = {"timeout": TIMEOUT_30SEC, "sleep_time": TIMEOUT_5SEC}
        return super().api_request(
            method=method,
            action=action,
            url=url or self._subresource_api_url,
            retry_params=retry_params or default_vmi_api_request_retry_params,
            **params,
        )

    def pause(self, timeout=TIMEOUT_4MINUTES, wait=False):
        self.api_request(method="PUT", action="pause")
        if wait:
            return self.wait_for_pause_status(pause=True, timeout=timeout)

    def unpause(self, timeout=TIMEOUT_4MINUTES, wait=False):
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
                dyn_client=self.client,
                namespace=self.namespace,
                label_selector=f"kubevirt.io=virt-launcher,kubevirt.io/created-by={self.instance.metadata.uid}",
            )
        )
        if not pods:
            raise ResourceNotFoundError(f"VIRT launcher POD not found for {self.kind}:{self.name}")

        migration_state = self.instance.status.migrationState
        if migration_state:
            #  After VM migration there are two pods, one in Completed status and one in Running status.
            #  We need to return the Pod that is not in Completed status.
            for pod in pods:
                if migration_state.targetPod == pod.name:
                    return pod
        else:
            return pods[0]

    @property
    def virt_handler_pod(self):
        pods = list(
            Pod.get(
                dyn_client=self.client,
                label_selector="kubevirt.io=virt-handler",
            )
        )
        for pod in pods:
            if pod.instance["spec"]["nodeName"] == self.instance.status.nodeName:
                return pod

        raise ResourceNotFoundError

    def wait_until_running(self, timeout=TIMEOUT_4MINUTES, logs=True, stop_status=None):
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
            self.wait_for_status(status=self.Status.RUNNING, timeout=timeout, stop_status=stop_status)
        except TimeoutExpiredError as sampler_ex:
            if not logs:
                raise
            try:
                virt_pod = self.virt_launcher_pod
                self.logger.error(f"Status of virt-launcher pod {virt_pod.name}: {virt_pod.status}")
                self.logger.debug(f"{virt_pod.name} *****LOGS*****")
                self.logger.debug(virt_pod.log(container="compute"))
            except ResourceNotFoundError as virt_pod_ex:
                self.logger.error(virt_pod_ex)
                raise sampler_ex

            raise

    def wait_for_pause_status(self, pause, timeout=TIMEOUT_4MINUTES):
        """
        Wait for Virtual Machine Instance to be paused / unpaused.
        Paused status is checked in libvirt and in the VMI conditions.

        Args:
            pause (bool): True for paused, False for unpause
            timeout (int): Time to wait for the resource.

        Raises:
            TimeoutExpiredError: If resource not exists.
        """
        self.logger.info(f"Wait until {self.kind} {self.name} is {'Paused' if pause else 'Unpuased'}")
        self.wait_for_domstate_pause_status(pause=pause, timeout=timeout)
        self.wait_for_vmi_condition_pause_status(pause=pause, timeout=timeout)

    def wait_for_domstate_pause_status(self, pause, timeout=TIMEOUT_4MINUTES):
        pause_status = "paused" if pause else "running"
        samples = TimeoutSampler(
            wait_timeout=timeout,
            sleep=1,
            exceptions_dict=PROTOCOL_ERROR_EXCEPTION_DICT,
            func=self.get_domstate,
        )
        for sample in samples:
            if pause_status in sample:
                return

    def wait_for_vmi_condition_pause_status(self, pause, timeout=TIMEOUT_4MINUTES):
        samples = TimeoutSampler(
            wait_timeout=timeout,
            sleep=1,
            exceptions_dict=PROTOCOL_ERROR_EXCEPTION_DICT,
            func=self.get_vmi_active_condition,
        )
        for sample in samples:
            # VM in state change
            # We have commanded a [un]pause condition via the API but the CR has not been updated yet to match.
            # 'reason' may not exist yet
            # or
            # 'reason' may still exist after unpause if the CR has not been updated before we perform this check
            if (pause and not sample.get("reason")) or (sample.get("reason") == "PausedByUser" and not pause):
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
            client=self.client,
            name=self.instance.status.nodeName,
        )

    def virsh_cmd(self, action):
        return shlex.split(
            f"virsh {self.virt_launcher_pod_hypervisor_connection_uri} {action} {self.namespace}_{self.name}"
        )

    def get_xml(self):
        """
        Get virtual machine instance XML

        Returns:
            xml_output(string): VMI XML in the multi-line string
        """
        return self.execute_virsh_command(command="dumpxml")

    @property
    def virt_launcher_pod_user_uid(self):
        """
        Get Virt Launcher Pod User UID value

        Returns:
            Int: Virt Launcher Pod UID value
        """
        return self.virt_launcher_pod.instance.spec.securityContext.runAsUser

    @property
    def is_virt_launcher_pod_root(self):
        """
        Check if Virt Launcher Pod is Root

        Returns:
            Bool: True if Virt Launcher Pod is Root.
        """
        return not bool(self.virt_launcher_pod_user_uid)

    @property
    def virt_launcher_pod_hypervisor_connection_uri(self):
        """
        Get Virt Launcher Pod Hypervisor Connection URI

        Required to connect to Hypervisor for
        Non-Root Virt-Launcher Pod.

        Returns:
            String: Hypervisor Connection URI
        """
        if self.is_virt_launcher_pod_root:
            hypervisor_connection_uri = ""
        else:
            virtqemud_socket = "virtqemud"
            socket = (
                virtqemud_socket
                if virtqemud_socket
                in self.virt_launcher_pod.execute(command=["ls", "/var/run/libvirt/"], container="compute")
                else "libvirt"
            )
            hypervisor_connection_uri = f"-c qemu+unix:///session?socket=/var/run/libvirt/{socket}-sock"
        return hypervisor_connection_uri

    def get_domstate(self):
        """
        Get virtual machine instance Status.

        Current workaround, as VM/VMI shows no status/phase == Paused yet.
        Bug: https://bugzilla.redhat.com/show_bug.cgi?id=1805178

        Returns:
            String: VMI Status as string
        """
        return self.execute_virsh_command(command="domstate")

    def get_dommemstat(self):
        """
        Get virtual machine domain memory stats
        link: https://libvirt.org/manpages/virsh.html#dommemstat

        Returns:
            String: VMI domain memory stats as string
        """
        return self.execute_virsh_command(command="dommemstat")

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
            self.logger.warning("Guest agent is not installed on the VM; OS version is not available.")
        return vmi_os_version

    def interface_ip(self, interface):
        iface_ip = [iface["ipAddress"] for iface in self.interfaces if iface["interfaceName"] == interface]
        return iface_ip[0] if iface_ip else None

    def execute_virsh_command(self, command):
        return self.virt_launcher_pod.execute(
            command=self.virsh_cmd(action=command),
            container="compute",
        )
