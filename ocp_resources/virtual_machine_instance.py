# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


import shlex
from typing import Any
from warnings import warn

import xmltodict
from kubernetes.dynamic import DynamicClient
from kubernetes.dynamic.exceptions import ResourceNotFoundError
from timeout_sampler import TimeoutExpiredError, TimeoutSampler

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.node import Node
from ocp_resources.pod import Pod
from ocp_resources.resource import NamespacedResource
from ocp_resources.utils.constants import (
    PROTOCOL_ERROR_EXCEPTION_DICT,
    TIMEOUT_4MINUTES,
    TIMEOUT_5SEC,
    TIMEOUT_30SEC,
)


class VirtualMachineInstance(NamespacedResource):
    """
    VirtualMachineInstance is *the* VirtualMachineInstance Definition. It represents a virtual machine in the runtime environment of kubernetes.
    """

    api_group: str = NamespacedResource.ApiGroup.KUBEVIRT_IO

    def __init__(
        self,
        access_credentials: list[Any] | None = None,
        affinity: dict[str, Any] | None = None,
        architecture: str | None = None,
        dns_config: dict[str, Any] | None = None,
        dns_policy: str | None = None,
        domain: dict[str, Any] | None = None,
        eviction_strategy: str | None = None,
        hostname: str | None = None,
        liveness_probe: dict[str, Any] | None = None,
        networks: list[Any] | None = None,
        node_selector: dict[str, Any] | None = None,
        priority_class_name: str | None = None,
        readiness_probe: dict[str, Any] | None = None,
        resource_claims: list[Any] | None = None,
        scheduler_name: str | None = None,
        start_strategy: str | None = None,
        subdomain: str | None = None,
        termination_grace_period_seconds: int | None = None,
        tolerations: list[Any] | None = None,
        topology_spread_constraints: list[Any] | None = None,
        volumes: list[Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            access_credentials (list[Any]): Specifies a set of public keys to inject into the vm guest

            affinity (dict[str, Any]): If affinity is specifies, obey all the affinity rules

            architecture (str): Specifies the architecture of the vm guest you are attempting to run.
              Defaults to the compiled architecture of the KubeVirt components

            dns_config (dict[str, Any]): Specifies the DNS parameters of a pod. Parameters specified here will
              be merged to the generated DNS configuration based on DNSPolicy.

            dns_policy (str): Set DNS policy for the pod. Defaults to "ClusterFirst". Valid values
              are 'ClusterFirstWithHostNet', 'ClusterFirst', 'Default' or
              'None'. DNS parameters given in DNSConfig will be merged with the
              policy selected with DNSPolicy. To have DNS options set along with
              hostNetwork, you have to specify DNS policy explicitly to
              'ClusterFirstWithHostNet'.

            domain (dict[str, Any]): Specification of the desired behavior of the VirtualMachineInstance on
              the host.

            eviction_strategy (str): EvictionStrategy describes the strategy to follow when a node drain
              occurs. The possible options are: - "None": No action will be
              taken, according to the specified 'RunStrategy' the VirtualMachine
              will be restarted or shutdown. - "LiveMigrate": the
              VirtualMachineInstance will be migrated instead of being shutdown.
              - "LiveMigrateIfPossible": the same as "LiveMigrate" but only if
              the VirtualMachine is Live-Migratable, otherwise it will behave as
              "None". - "External": the VirtualMachineInstance will be protected
              and 'vmi.Status.EvacuationNodeName' will be set on eviction. This
              is mainly useful for cluster-api-provider-kubevirt (capk) which
              needs a way for VMI's to be blocked from eviction, yet signal capk
              that eviction has been called on the VMI so the capk controller
              can handle tearing the VMI down. Details can be found in the
              commit description https://github.com/kubevirt/kubevirt/commit/c1d
              77face705c8b126696bac9a3ee3825f27f1fa.

            hostname (str): Specifies the hostname of the vmi If not specified, the hostname will
              be set to the name of the vmi, if dhcp or cloud-init is configured
              properly.

            liveness_probe (dict[str, Any]): Periodic probe of VirtualMachineInstance liveness.
              VirtualmachineInstances will be stopped if the probe fails. Cannot
              be updated. More info:
              https://kubernetes.io/docs/concepts/workloads/pods/pod-
              lifecycle#container-probes

            networks (list[Any]): List of networks that can be attached to a vm's virtual interface.

            node_selector (dict[str, Any]): NodeSelector is a selector which must be true for the vmi to fit on a
              node. Selector which must match a node's labels for the vmi to be
              scheduled on that node. More info:
              https://kubernetes.io/docs/concepts/configuration/assign-pod-node/

            priority_class_name (str): If specified, indicates the pod's priority. If not specified, the pod
              priority will be default or zero if there is no default.

            readiness_probe (dict[str, Any]): Periodic probe of VirtualMachineInstance service readiness.
              VirtualmachineInstances will be removed from service endpoints if
              the probe fails. Cannot be updated. More info:
              https://kubernetes.io/docs/concepts/workloads/pods/pod-
              lifecycle#container-probes

            resource_claims (list[Any]): ResourceClaims define which ResourceClaims must be allocated and
              reserved before the VMI, hence virt-launcher pod is allowed to
              start. The resources will be made available to the domain which
              consumes them by name.  This is an alpha field and requires
              enabling the DynamicResourceAllocation feature gate in kubernetes
              https://kubernetes.io/docs/concepts/scheduling-eviction/dynamic-
              resource-allocation/ This field should only be configured if one
              of the feature-gates GPUsWithDRA or HostDevicesWithDRA is enabled.
              This feature is in alpha.

            scheduler_name (str): If specified, the VMI will be dispatched by specified scheduler. If
              not specified, the VMI will be dispatched by default scheduler.

            start_strategy (str): StartStrategy can be set to "Paused" if Virtual Machine should be
              started in paused state.

            subdomain (str): If specified, the fully qualified vmi hostname will be
              "<hostname>.<subdomain>.<pod namespace>.svc.<cluster domain>". If
              not specified, the vmi will not have a domainname at all. The DNS
              entry will resolve to the vmi, no matter if the vmi itself can
              pick up a hostname.

            termination_grace_period_seconds (int): Grace period observed after signalling a VirtualMachineInstance to
              stop after which the VirtualMachineInstance is force terminated.

            tolerations (list[Any]): If toleration is specified, obey all the toleration rules.

            topology_spread_constraints (list[Any]): TopologySpreadConstraints describes how a group of VMIs will be spread
              across a given topology domains. K8s scheduler will schedule VMI
              pods in a way which abides by the constraints.

            volumes (list[Any]): List of volumes that can be mounted by disks belonging to the vmi.

        """
        super().__init__(**kwargs)

        self.access_credentials = access_credentials
        self.affinity = affinity
        self.architecture = architecture
        self.dns_config = dns_config
        self.dns_policy = dns_policy
        self.domain = domain
        self.eviction_strategy = eviction_strategy
        self.hostname = hostname
        self.liveness_probe = liveness_probe
        self.networks = networks
        self.node_selector = node_selector
        self.priority_class_name = priority_class_name
        self.readiness_probe = readiness_probe
        self.resource_claims = resource_claims
        self.scheduler_name = scheduler_name
        self.start_strategy = start_strategy
        self.subdomain = subdomain
        self.termination_grace_period_seconds = termination_grace_period_seconds
        self.tolerations = tolerations
        self.topology_spread_constraints = topology_spread_constraints
        self.volumes = volumes

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.domain is None:
                raise MissingRequiredArgumentError(argument="self.domain")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["domain"] = self.domain

            if self.access_credentials is not None:
                _spec["accessCredentials"] = self.access_credentials

            if self.affinity is not None:
                _spec["affinity"] = self.affinity

            if self.architecture is not None:
                _spec["architecture"] = self.architecture

            if self.dns_config is not None:
                _spec["dnsConfig"] = self.dns_config

            if self.dns_policy is not None:
                _spec["dnsPolicy"] = self.dns_policy

            if self.eviction_strategy is not None:
                _spec["evictionStrategy"] = self.eviction_strategy

            if self.hostname is not None:
                _spec["hostname"] = self.hostname

            if self.liveness_probe is not None:
                _spec["livenessProbe"] = self.liveness_probe

            if self.networks is not None:
                _spec["networks"] = self.networks

            if self.node_selector is not None:
                _spec["nodeSelector"] = self.node_selector

            if self.priority_class_name is not None:
                _spec["priorityClassName"] = self.priority_class_name

            if self.readiness_probe is not None:
                _spec["readinessProbe"] = self.readiness_probe

            if self.resource_claims is not None:
                _spec["resourceClaims"] = self.resource_claims

            if self.scheduler_name is not None:
                _spec["schedulerName"] = self.scheduler_name

            if self.start_strategy is not None:
                _spec["startStrategy"] = self.start_strategy

            if self.subdomain is not None:
                _spec["subdomain"] = self.subdomain

            if self.termination_grace_period_seconds is not None:
                _spec["terminationGracePeriodSeconds"] = self.termination_grace_period_seconds

            if self.tolerations is not None:
                _spec["tolerations"] = self.tolerations

            if self.topology_spread_constraints is not None:
                _spec["topologySpreadConstraints"] = self.topology_spread_constraints

            if self.volumes is not None:
                _spec["volumes"] = self.volumes

    # End of generated code

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
            self.wait_for_pause_status(pause=True, timeout=timeout)

    def unpause(self, timeout=TIMEOUT_4MINUTES, wait=False):
        self.api_request(method="PUT", action="unpause")
        if wait:
            self.wait_for_pause_status(pause=False, timeout=timeout)

    def reset(self) -> dict[str, Any]:
        return self.api_request(method="PUT", action="reset")

    @property
    def interfaces(self):
        return self.instance.status.interfaces

    def get_virt_launcher_pod(self, privileged_client: DynamicClient | None = None) -> Pod:
        """Get the virt-launcher pod for this VMI.

        Args:
            privileged_client: Client with elevated privileges for pod listing.

        Returns:
            Pod: The virt-launcher pod.

        Raises:
            ResourceNotFoundError: If no virt-launcher pod is found.
        """
        pods = list(
            Pod.get(
                client=privileged_client or self.client,
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

        return pods[0]

    @property
    def virt_launcher_pod(self) -> Pod:
        warn(
            "'virt_launcher_pod' property is deprecated, use 'get_virt_launcher_pod' instead.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        return self.get_virt_launcher_pod(privileged_client=self.client)

    def get_virt_handler_pod(self, privileged_client: DynamicClient | None = None) -> Pod:
        """Get the virt-handler pod running on the same node as this VMI.

        Args:
            privileged_client: Client with elevated privileges for pod listing.

        Returns:
            Pod: The virt-handler pod.

        Raises:
            ResourceNotFoundError: If no matching virt-handler pod is found.
        """
        pods = list(
            Pod.get(
                client=privileged_client or self.client,
                label_selector="kubevirt.io=virt-handler",
            )
        )
        for pod in pods:
            if pod.instance["spec"]["nodeName"] == self.instance.status.nodeName:
                return pod

        raise ResourceNotFoundError(f"virt-handler pod not found on node {self.instance.status.nodeName}")

    @property
    def virt_handler_pod(self) -> Pod:
        warn(
            "'virt_handler_pod' property is deprecated, use 'get_virt_handler_pod' instead.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        return self.get_virt_handler_pod(privileged_client=self.client)

    def wait_until_running(
        self,
        timeout: int = TIMEOUT_4MINUTES,
        logs: bool = True,
        stop_status: str | None = None,
        privileged_client: DynamicClient | None = None,
    ) -> None:
        """
        Wait until VMI is running

        Args:
            timeout (int): Time to wait for VMI.
            logs (bool): True to extract logs from the VMI pod and from the VMI.
            stop_status (str): Status which should stop the wait and failed.
            privileged_client: Client with elevated privileges for error-path pod access.

        Raises:
            TimeoutExpiredError: If VMI failed to run.
        """
        try:
            self.wait_for_status(status=self.Status.RUNNING, timeout=timeout, stop_status=stop_status)
        except TimeoutExpiredError as sampler_ex:
            if not logs:
                raise
            try:
                virt_pod = self.get_virt_launcher_pod(privileged_client=privileged_client or self.client)
                self.logger.error(f"Status of virt-launcher pod {virt_pod.name}: {virt_pod.status}")
                self.logger.debug(f"{virt_pod.name} *****LOGS*****")
                self.logger.debug(virt_pod.log(container="compute"))
            except ResourceNotFoundError as virt_pod_ex:
                self.logger.error(virt_pod_ex)
                raise sampler_ex from virt_pod_ex

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
        self.wait_for_vmi_condition_pause_status(pause=pause, timeout=timeout)

    def wait_for_domstate_pause_status(self, pause, timeout=TIMEOUT_4MINUTES):
        warn(
            message="wait_for_domstate_pause_status is deprecated and will be removed the next version.",
            category=DeprecationWarning,
            stacklevel=2,
        )
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

    def get_node(self, privileged_client: DynamicClient | None = None) -> Node:
        """Get the node where this VMI is running.

        Args:
            privileged_client: Client with elevated privileges for node access.

        Returns:
            Node: The node running this VMI.
        """
        return Node(
            client=privileged_client or self.client,
            name=self.instance.status.nodeName,
        )

    @property
    def node(self) -> Node:
        """
        Get the node name where the VM is running

        Returns:
            Node: Node
        """
        warn(
            "'node' property is deprecated, use 'get_node' instead.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        return self.get_node(privileged_client=self.client)

    @staticmethod
    def get_pod_user_uid(pod: Pod) -> int | None:
        """Get the runAsUser UID from a pod's security context.

        Args:
            pod: The pod to inspect.

        Returns:
            int | None: The runAsUser UID value, or None if not set.
        """
        security_context = pod.instance.spec.get("securityContext", {})
        if security_context:
            return security_context.get("runAsUser")
        return None

    @staticmethod
    def is_pod_root(pod: Pod) -> bool:
        """Check if a pod runs as root.

        Args:
            pod: The pod to inspect.

        Returns:
            bool: True if the pod runs as root (UID 0 or unset).
        """
        uid = VirtualMachineInstance.get_pod_user_uid(pod=pod)
        # In KubeVirt, virt-launcher pods without explicit runAsUser run as root (UID 0).
        return uid is None or uid == 0

    @staticmethod
    def get_hypervisor_connection_uri(pod: Pod) -> str:
        """Get the hypervisor connection URI for a pod.

        Note: This method executes a remote command on the pod to detect the libvirt socket type.

        Args:
            pod: The virt-launcher pod.

        Returns:
            str: The hypervisor connection URI string.
        """
        if VirtualMachineInstance.is_pod_root(pod=pod):
            return ""

        virtqemud_socket = "virtqemud"
        socket = (
            virtqemud_socket
            if virtqemud_socket in pod.execute(command=["ls", "/var/run/libvirt/"], container="compute")
            else "libvirt"
        )
        return f"-c qemu+unix:///session?socket=/var/run/libvirt/{socket}-sock"

    def virsh_cmd(
        self, action: str, privileged_client: DynamicClient | None = None, pod: Pod | None = None
    ) -> list[str]:
        """Build a virsh command list for the given action.

        Args:
            action: The virsh action to perform (e.g., 'dumpxml', 'domstate').
            privileged_client: Client with elevated privileges.
            pod: Optional virt-launcher pod (avoids re-fetching if already available).

        Returns:
            list[str]: The command as a list of strings.
        """
        # For backward compatibility
        if pod is None:
            pod = self.get_virt_launcher_pod(privileged_client=privileged_client or self.client)

        hypervisor_uri = self.get_hypervisor_connection_uri(pod=pod)
        return shlex.split(f"virsh {hypervisor_uri} {action} {self.namespace}_{self.name}")

    def get_xml(self, privileged_client: DynamicClient | None = None) -> str:
        """
        Get virtual machine instance XML

        Args:
            privileged_client: Client with elevated privileges.

        Returns:
            xml_output(string): VMI XML in the multi-line string
        """
        return self.execute_virsh_command(command="dumpxml", privileged_client=privileged_client)

    @property
    def virt_launcher_pod_user_uid(self) -> int | None:
        warn(
            "'virt_launcher_pod_user_uid' property is deprecated, use 'get_pod_user_uid' instead.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        return self.get_pod_user_uid(pod=self.get_virt_launcher_pod(privileged_client=self.client))

    @property
    def is_virt_launcher_pod_root(self) -> bool:
        warn(
            "'is_virt_launcher_pod_root' property is deprecated, use 'is_pod_root' instead.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        return self.is_pod_root(pod=self.get_virt_launcher_pod(privileged_client=self.client))

    @property
    def virt_launcher_pod_hypervisor_connection_uri(self) -> str:
        warn(
            "'virt_launcher_pod_hypervisor_connection_uri' property is deprecated, "
            "use 'get_hypervisor_connection_uri' instead.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        return self.get_hypervisor_connection_uri(pod=self.get_virt_launcher_pod(privileged_client=self.client))

    def get_domstate(self, privileged_client: DynamicClient | None = None) -> str:
        """
        Get virtual machine instance Status.

        Current workaround, as VM/VMI shows no status/phase == Paused yet.
        Bug: https://bugzilla.redhat.com/show_bug.cgi?id=1805178

        Args:
            privileged_client: Client with elevated privileges.

        Returns:
            String: VMI Status as string
        """
        warn(
            message="get_domstate is deprecated and will be removed the next version.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        return self.execute_virsh_command(command="domstate", privileged_client=privileged_client)

    def get_dommemstat(self, privileged_client: DynamicClient | None = None) -> str:
        """
        Get virtual machine domain memory stats
        link: https://libvirt.org/manpages/virsh.html#dommemstat

        Args:
            privileged_client: Client with elevated privileges.

        Returns:
            String: VMI domain memory stats as string
        """
        return self.execute_virsh_command(command="dommemstat", privileged_client=privileged_client)

    def get_vmi_active_condition(self):
        """A VMI may have multiple conditions; the active one it the one with
        'lastTransitionTime'"""
        return {
            k: v
            for condition in self.instance.status.conditions
            for k, v in condition.items()
            if condition["lastTransitionTime"]
        }

    def get_xml_dict(self, privileged_client: DynamicClient | None = None) -> dict[str, Any]:
        """Get virtual machine instance XML as dict.

        Args:
            privileged_client: Client with elevated privileges.

        Returns:
            dict: Parsed XML of the VMI.
        """
        return xmltodict.parse(xml_input=self.get_xml(privileged_client=privileged_client), process_namespaces=True)

    @property
    def xml_dict(self) -> dict[str, Any]:
        """Get virtual machine instance XML as dict"""
        warn(
            "'xml_dict' property is deprecated, use 'get_xml_dict' instead.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        return self.get_xml_dict(privileged_client=self.client)

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

    def execute_virsh_command(self, command: str, privileged_client: DynamicClient | None = None) -> str:
        """Execute a virsh command in the virt-launcher pod.

        Args:
            command: The virsh command to execute (e.g., 'dumpxml', 'domstate').
            privileged_client: Client with elevated privileges.

        Returns:
            str: Command output.
        """
        pod = self.get_virt_launcher_pod(privileged_client=privileged_client or self.client)
        return pod.execute(
            command=self.virsh_cmd(action=command, pod=pod),
            container="compute",
        )
