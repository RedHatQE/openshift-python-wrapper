import re

from openshift.dynamic.exceptions import ConflictError

from ocp_resources.node_network_configuration_enactment import (
    NodeNetworkConfigurationEnactment,
)
from ocp_resources.node_network_state import NodeNetworkState
from ocp_resources.resource import Resource
from ocp_resources.utils import TimeoutExpiredError, TimeoutSampler


class NNCPConfigurationFailed(Exception):
    pass


class NodeNetworkConfigurationPolicy(Resource):
    api_group = Resource.ApiGroup.NMSTATE_IO

    class Conditions:
        class Type:
            FAILING = "Failing"
            AVAILABLE = "Available"
            PROGRESSING = "Progressing"
            MATCHING = "Matching"

        class Reason:
            CONFIGURING = "ConfigurationProgressing"
            SUCCESS = "SuccessfullyConfigured"
            FAILED = "FailedToConfigure"
            NO_MATCHING_NODE = "NoMatchingNode"

    def __init__(
        self,
        name,
        client=None,
        worker_pods=None,
        node_selector=None,
        teardown=True,
        mtu=None,
        ports=None,
        ipv4_enable=False,
        ipv4_dhcp=False,
        ipv4_addresses=None,
        ipv6_enable=False,
        node_active_nics=None,
        dns_resolver=None,
        routes=None,
    ):
        """
        ipv4_addresses should be sent in this format:
        [{"ip": <ip1-string>, "prefix-length": <prefix-len1-int>},
         {"ip": <ip2-string>, "prefix-length": <prefix-len2-int>}, ...]
        For example:
        [{"ip": "10.1.2.3", "prefix-length": 24},
         {"ip": "10.4.5.6", "prefix-length": 24},
         {"ip": "10.7.8.9", "prefix-length": 23}]
        """
        super().__init__(name=name, client=client, teardown=teardown)
        self.desired_state = {"interfaces": []}
        self.worker_pods = worker_pods
        self.mtu = mtu
        self.mtu_dict = {}
        self.ports = ports or []
        self.iface = None
        self.ifaces = []
        self.node_active_nics = node_active_nics or []
        self.ipv4_enable = ipv4_enable
        self._ipv4_dhcp = ipv4_dhcp
        self.ipv4_addresses = ipv4_addresses or []
        self.ipv6_enable = ipv6_enable
        self.ipv4_iface_state = {}
        self.node_selector = node_selector
        self.dns_resolver = dns_resolver
        self.routes = routes
        if self.node_selector:
            self._node_selector = {
                f"{self.ApiGroup.KUBERNETES_IO}/hostname": self.node_selector
            }
            if self.worker_pods:
                for pod in self.worker_pods:
                    if pod.node.name == node_selector:
                        self.worker_pods = [pod]
                        break
        else:
            self._node_selector = {
                f"node-role.{self.ApiGroup.KUBERNETES_IO}/worker": ""
            }

    def set_interface(self, interface):
        # First drop the interface if it's already in the list
        interfaces = [
            iface
            for iface in self.desired_state["interfaces"]
            if not (iface["name"] == interface["name"])
        ]
        # Add the interface
        interfaces.append(interface)
        self.desired_state["interfaces"] = interfaces

    def to_dict(self):
        res = super().to_dict()
        if self.dns_resolver or self.routes or self.iface:
            res.setdefault("spec", {}).setdefault("desiredState", {})

        if self._node_selector:
            res.setdefault("spec", {}).setdefault("nodeSelector", self._node_selector)

        if self.dns_resolver:
            res["spec"]["desiredState"]["dns-resolver"] = self.dns_resolver

        if self.routes:
            res["spec"]["desiredState"]["routes"] = self.routes

        if self.iface:
            """
            It's the responsibility of the caller to verify the desired configuration they send.
            For example: "ipv4.dhcp.enabled: false" without specifying any static IP address
            is a valid desired state and therefore not blocked in the code, but nmstate would
            reject it. Such configuration might be used for negative tests.
            """
            self.iface["ipv4"] = {"enabled": self.ipv4_enable, "dhcp": self.ipv4_dhcp}
            if self.ipv4_addresses:
                self.iface["ipv4"]["address"] = self.ipv4_addresses

            self.iface["ipv6"] = {"enabled": self.ipv6_enable}

            self.set_interface(interface=self.iface)
            if self.iface["name"] not in [_iface["name"] for _iface in self.ifaces]:
                self.ifaces.append(self.iface)

            res["spec"]["desiredState"]["interfaces"] = self.desired_state["interfaces"]

        return res

    def apply(self, resource=None):
        resource = resource if resource else super().to_dict()
        samples = TimeoutSampler(
            wait_timeout=3,
            sleep=1,
            exceptions=ConflictError,
            func=self.update,
            resource_dict=resource,
        )
        self.logger.info(f"Applying {resource}")
        for _ in samples:
            return

    def deploy(self):
        if self._ipv4_dhcp:
            self._ipv4_state_backup()

        if self.mtu:
            for pod in self.worker_pods:
                for port in self.ports:
                    mtu = pod.execute(
                        command=["cat", f"/sys/class/net/{port}/mtu"]
                    ).strip()
                    self.logger.info(
                        f"Backup MTU: {pod.node.name} interface {port} MTU is {mtu}"
                    )
                    self.mtu_dict[port] = mtu

        self.create()

        try:
            self.wait_for_status_success()
            self.validate_create()
            return self
        except Exception as e:
            self.logger.error(e)
            self.clean_up()
            raise

    @property
    def ipv4_dhcp(self):
        return self._ipv4_dhcp

    @ipv4_dhcp.setter
    def ipv4_dhcp(self, ipv4_dhcp):
        if ipv4_dhcp != self._ipv4_dhcp:
            self._ipv4_dhcp = ipv4_dhcp

            if self._ipv4_dhcp:
                self._ipv4_state_backup()
                self.iface["ipv4"] = {"dhcp": True, "enabled": True}

            self.set_interface(interface=self.iface)
            self.apply()

    def clean_up(self):
        if self.mtu:
            for port in self.ports:
                _port = {
                    "name": port,
                    "type": "ethernet",
                    "state": self.Interface.State.UP,
                    "mtu": int(self.mtu_dict[port]),
                }
                self.set_interface(interface=_port)

        for iface in self.ifaces:
            """
            If any physical interfaces are part of the policy - we will skip them,
            because we don't want to delete them (and we actually can't, and this attempt
            would end with failure).
            """
            if iface["name"] in self.node_active_nics:
                continue
            try:
                self._absent_interface()
                self.wait_for_status_success()
                self.wait_for_interface_deleted()
            except Exception as e:
                self.logger.error(e)

        super().clean_up()

    def wait_for_interface_deleted(self):
        if self.worker_pods:
            for pod in self.worker_pods:
                for iface in self.ifaces:
                    iface_name = iface["name"]
                    node_network_state = NodeNetworkState(name=pod.node.name)
                    iface_dict = node_network_state.get_interface(name=iface_name)
                    if iface_dict.get("type") == "ethernet":
                        self.logger.info(f"{iface_name} is type ethernet, skipping.")
                        continue

                    node_network_state.wait_until_deleted(name=iface_name)

    def validate_create(self):
        if self.worker_pods:
            for pod in self.worker_pods:
                for bridge in self.ifaces:
                    node_network_state = NodeNetworkState(name=pod.node.name)
                    node_network_state.wait_until_up(name=bridge["name"])

    def _ipv4_state_backup(self):
        # Backup current state of dhcp for the interfaces which arent veth or current bridge
        for pod in self.worker_pods:
            node_network_state = NodeNetworkState(name=pod.node.name)
            self.ipv4_iface_state[pod.node.name] = {}
            for interface in node_network_state.instance.status.currentState.interfaces:
                if interface["name"] in self.ports:
                    self.ipv4_iface_state[pod.node.name].update(
                        {
                            interface["name"]: {
                                k: interface["ipv4"][k] for k in ("dhcp", "enabled")
                            }
                        }
                    )

    def _absent_interface(self):
        for bridge in self.ifaces:
            bridge["state"] = self.Interface.State.ABSENT
            self.set_interface(interface=bridge)

            if self._ipv4_dhcp:
                temp_ipv4_iface_state = {}
                for pod in self.worker_pods:
                    node_network_state = NodeNetworkState(name=pod.node.name)
                    temp_ipv4_iface_state[pod.node.name] = {}
                    # Find which interfaces got changed (of those that are connected to bridge)
                    for (
                        interface
                    ) in node_network_state.instance.status.currentState.interfaces:
                        if interface["name"] in self.ports:
                            x = {k: interface["ipv4"][k] for k in ("dhcp", "enabled")}
                            if (
                                self.ipv4_iface_state[pod.node.name][interface["name"]]
                                != x
                            ):
                                temp_ipv4_iface_state[pod.node.name].update(
                                    {
                                        interface["name"]: self.ipv4_iface_state[
                                            pod.node.name
                                        ][interface["name"]]
                                    }
                                )

                previous_state = next(iter(temp_ipv4_iface_state.values()))

                # Restore DHCP state of the changed bridge connected ports
                for iface_name, ipv4 in previous_state.items():
                    interface = {"name": iface_name, "ipv4": ipv4}
                    self.set_interface(interface=interface)

        self.apply(resource=self._resource_dict_for_cleanup())

    def status(self):
        for condition in self.instance.status.conditions:
            if condition["type"] == self.Conditions.Type.AVAILABLE:
                return condition["reason"]

    def wait_for_configuration_conditions_unknown_or_progressing(self, wait_timeout=30):
        samples = TimeoutSampler(
            wait_timeout=wait_timeout,
            sleep=1,
            func=lambda: self.instance.status.conditions,
        )
        for sample in samples:
            if (
                sample
                and sample[0]["type"] == self.Conditions.Type.AVAILABLE
                and (
                    sample[0]["status"] == self.Condition.Status.UNKNOWN
                    or sample[0]["reason"] == self.Conditions.Reason.CONFIGURING
                )
            ):
                return sample

    def wait_for_status_success(self):
        failed_condition_reason = self.Conditions.Reason.FAILED
        no_match_node_condition_reason = self.Conditions.Reason.NO_MATCHING_NODE

        def _process_failed_status():
            last_err_msg = None
            for failed_nnce in self._get_failed_nnce():
                nnce_name = failed_nnce.instance.metadata.name
                nnce_dict = failed_nnce.instance.to_dict()
                for cond in nnce_dict["status"]["conditions"]:
                    err_msg = self._get_nnce_error_msg(
                        nnce_name=nnce_name, nnce_condition=cond
                    )
                    if err_msg:
                        last_err_msg = err_msg

            raise NNCPConfigurationFailed(
                f"Reason: {failed_condition_reason}\n{last_err_msg}"
            )

        # if we get here too fast there are no conditions, we need to wait.
        self.wait_for_configuration_conditions_unknown_or_progressing()

        samples = TimeoutSampler(wait_timeout=480, sleep=1, func=self.status)
        try:
            for sample in samples:
                if sample == self.Conditions.Reason.SUCCESS:
                    self.logger.info(f"NNCP {self.name} configured Successfully")
                    return sample

                elif sample == no_match_node_condition_reason:
                    raise NNCPConfigurationFailed(
                        f"{self.name}. Reason: {no_match_node_condition_reason}"
                    )

                elif sample == failed_condition_reason:
                    _process_failed_status()

        except (TimeoutExpiredError, NNCPConfigurationFailed):
            self.logger.error(
                f"Unable to configure NNCP {self.name} for node {self.node_selector}"
            )
            raise

    @staticmethod
    def _get_nnce_error_msg(nnce_name, nnce_condition):
        err_msg = ""
        nnce_prefix = f"NNCE {nnce_name}"
        nnce_msg = nnce_condition.get("message")
        if not nnce_msg:
            return err_msg

        errors = nnce_msg.split("->")
        if errors:
            err_msg += f"{nnce_prefix}: {errors[0]}"
            if len(errors) > 1:
                err_msg += errors[-1]

        libnmstate_err = re.findall(r"libnmstate.error.*", nnce_msg)
        if libnmstate_err:
            err_msg += f"{nnce_prefix }: {libnmstate_err[0]}"

        return err_msg

    def _get_failed_nnce(self):
        for nnce in NodeNetworkConfigurationEnactment.get(dyn_client=self.client):
            try:
                nnce.wait_for_conditions()
            except TimeoutExpiredError:
                self.logger.error(f"Failed to get NNCE {nnce.name} status")
                continue

            for nnce_cond in nnce.instance.status.conditions:
                if (
                    nnce_cond.type == "Failing"
                    and nnce_cond.status == Resource.Condition.Status.TRUE
                ):
                    yield nnce

    def _resource_dict_for_cleanup(self):
        resource_dict = self.to_dict()
        desired_state = {"interfaces": self.ifaces}
        resource_dict.update({"spec": {"desiredState": desired_state}})
        if self.routes:
            resource_dict["spec"]["desiredState"]["routes"] = None

        return resource_dict
