import re

from openshift.dynamic.exceptions import ConflictError

from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.node import Node
from ocp_resources.node_network_configuration_enactment import (
    NodeNetworkConfigurationEnactment,
)
from ocp_resources.node_network_state import NodeNetworkState
from ocp_resources.resource import Resource, ResourceEditor
from ocp_resources.utils import TimeoutExpiredError, TimeoutSampler


class NNCPConfigurationFailed(Exception):
    pass


class NodeNetworkConfigurationPolicy(Resource):
    api_group = Resource.ApiGroup.NMSTATE_IO

    class Conditions:
        class Type:
            DEGRADED = "Degraded"
            AVAILABLE = "Available"

        class Reason:
            CONFIGURATION_PROGRESSING = "ConfigurationProgressing"
            SUCCESSFULLY_CONFIGURED = "SuccessfullyConfigured"
            FAILED_TO_CONFIGURE = "FailedToConfigure"
            NO_MATCHING_NODE = "NoMatchingNode"

    def __init__(
        self,
        name=None,
        client=None,
        capture=None,
        node_selector=None,
        node_selector_labels=None,
        teardown_absent_ifaces=True,
        teardown=True,
        mtu=None,
        ports=None,
        ipv4_enable=False,
        ipv4_dhcp=False,
        ipv4_auto_dns=True,
        ipv4_addresses=None,
        ipv6_enable=False,
        ipv6_dhcp=False,
        ipv6_auto_dns=True,
        ipv6_addresses=None,
        dns_resolver=None,
        routes=None,
        yaml_file=None,
        set_ipv4=True,
        set_ipv6=True,
        max_unavailable=None,
        state=None,
        success_timeout=480,
        delete_timeout=TIMEOUT_4MINUTES,
        **kwargs,
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
        super().__init__(
            name=name,
            client=client,
            teardown=teardown,
            yaml_file=yaml_file,
            delete_timeout=delete_timeout,
            node_selector=node_selector,
            node_selector_labels=node_selector_labels,
            **kwargs,
        )
        self.desired_state = {"interfaces": []}
        self.mtu = mtu
        self.capture = capture
        self.mtu_dict = {}
        self.ports = ports or []
        self.iface = None
        self.ipv4_enable = ipv4_enable
        self.ipv4_dhcp = ipv4_dhcp
        self.ipv4_auto_dns = ipv4_auto_dns
        self.ipv4_addresses = ipv4_addresses or []
        self.ipv4_iface_state = {}
        self.ipv6_enable = ipv6_enable
        self.ipv6_dhcp = ipv6_dhcp
        self.ipv6_autoconf = self.ipv6_dhcp
        self.ipv6_auto_dns = ipv6_auto_dns
        self.ipv6_addresses = ipv6_addresses
        self.dns_resolver = dns_resolver
        self.routes = routes
        self.state = state or self.Interface.State.UP
        self.set_ipv4 = set_ipv4
        self.set_ipv6 = set_ipv6
        self.success_timeout = success_timeout
        self.max_unavailable = max_unavailable
        self.ipv4_ports_backup_dict = {}
        self.ipv6_ports_backup_dict = {}
        self.nodes = self._nodes()
        self.teardown_absent_ifaces = teardown_absent_ifaces

    def _nodes(self):
        if self.node_selector:
            return list(Node.get(dyn_client=self.client, name=self.node_selector))
        if self.node_selector_labels:
            node_labels = ",".join(
                [
                    f"{label_key}={label_value}"
                    for label_key, label_value in self.node_selector_labels.items()
                ]
            )
            return list(Node.get(dyn_client=self.client, label_selector=node_labels))

    def set_interface(self, interface):
        if not self.res:
            super().to_dict()
        # First drop the interface if it's already in the list
        interfaces = [
            iface
            for iface in self.desired_state["interfaces"]
            if iface["name"] != interface["name"]
        ]
        # Add the interface
        interfaces.append(interface)
        self.desired_state["interfaces"] = interfaces
        self.res.setdefault("spec", {}).setdefault("desiredState", {})[
            "interfaces"
        ] = self.desired_state["interfaces"]

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file:
            if self.dns_resolver or self.routes or self.iface:
                self.res.setdefault("spec", {}).setdefault("desiredState", {})

            if self.node_selector_spec:
                self.res.setdefault("spec", {}).setdefault(
                    "nodeSelector", self.node_selector_spec
                )

            if self.capture:
                self.res["spec"]["capture"] = self.capture

            if self.dns_resolver:
                self.res["spec"]["desiredState"]["dns-resolver"] = self.dns_resolver

            if self.routes:
                self.res["spec"]["desiredState"]["routes"] = self.routes

            if self.max_unavailable:
                self.res.setdefault("spec", {}).setdefault(
                    "maxUnavailable", self.max_unavailable
                )

            if self.iface:
                """
                It's the responsibility of the caller to verify the desired configuration they send.
                For example: "ipv4.dhcp.enabled: false" without specifying any static IP address
                is a valid desired state and therefore not blocked in the code, but nmstate would
                reject it. Such configuration might be used for negative tests.
                """
                self.res = self.add_interface(
                    iface=self.iface,
                    state=self.state,
                    set_ipv4=self.set_ipv4,
                    ipv4_enable=self.ipv4_enable,
                    ipv4_dhcp=self.ipv4_dhcp,
                    ipv4_auto_dns=self.ipv4_auto_dns,
                    ipv4_addresses=self.ipv4_addresses,
                    set_ipv6=self.set_ipv6,
                    ipv6_enable=self.ipv6_enable,
                    ipv6_dhcp=self.ipv6_dhcp,
                    ipv6_auto_dns=self.ipv6_auto_dns,
                    ipv6_addresses=self.ipv6_addresses,
                    ipv6_autoconf=self.ipv6_autoconf,
                )

    def add_interface(
        self,
        iface=None,
        name=None,
        type_=None,
        state=None,
        set_ipv4=True,
        ipv4_enable=False,
        ipv4_dhcp=False,
        ipv4_auto_dns=True,
        ipv4_addresses=None,
        set_ipv6=True,
        ipv6_enable=False,
        ipv6_dhcp=False,
        ipv6_auto_dns=True,
        ipv6_addresses=None,
        ipv6_autoconf=False,
    ):
        #  If self.res is already defined (from to_dict()), don't call it again.
        if not self.res:
            self.to_dict()

        self.res.setdefault("spec", {}).setdefault("desiredState", {})
        if not iface:
            iface = {
                "name": name,
                "type": type_,
                "state": state,
            }
        if set_ipv4:
            if isinstance(set_ipv4, str):
                iface["ipv4"] = set_ipv4

            else:
                iface["ipv4"] = {
                    "enabled": ipv4_enable,
                    "dhcp": ipv4_dhcp,
                    "auto-dns": ipv4_auto_dns,
                }
                if ipv4_addresses:
                    iface["ipv4"]["address"] = ipv4_addresses

        if set_ipv6:
            if isinstance(set_ipv6, str):
                iface["ipv6"] = set_ipv6

            else:
                iface["ipv6"] = {
                    "enabled": ipv6_enable,
                    "dhcp": ipv6_dhcp,
                    "auto-dns": ipv6_auto_dns,
                    "autoconf": ipv6_autoconf,
                }
                if ipv6_addresses:
                    iface["ipv6"]["address"] = ipv6_addresses

        self.set_interface(interface=iface)
        return self.res

    def _get_port_from_nns(self, port_name):
        if not self.nodes:
            return None

        nns = NodeNetworkState(name=self.nodes[0].name)
        _port = [_iface for _iface in nns.interfaces if _iface["name"] == port_name]
        return _port[0] if _port else None

    def _ports_backup(self, ip_family):
        for port in self.ports:
            _port = self._get_port_from_nns(port_name=port)
            if _port:
                self.ipv4_ports_backup_dict[port] = _port[ip_family]

    def ipv4_ports_backup(self):
        self._ports_backup(ip_family="ipv4")

    def ipv6_ports_backup(self):
        self._ports_backup(ip_family="ipv6")

    def add_ports(self):
        for port in self.ports:
            _port = self._get_port_from_nns(port_name=port)
            if _port:
                ipv4_backup = self.ipv4_ports_backup_dict.get(port)
                ipv6_backup = self.ipv6_ports_backup_dict.get(port)
                if ipv4_backup or ipv6_backup:
                    iface = {
                        "name": port,
                        "type": _port["type"],
                        "state": _port["state"],
                    }
                    if ipv4_backup:
                        iface["ipv4"] = ipv4_backup

                    if ipv6_backup:
                        iface["ipv6"] = ipv6_backup

                    self.set_interface(interface=iface)

    def apply(self, resource=None):
        if not resource:
            super().to_dict()
            resource = self.res
        samples = TimeoutSampler(
            wait_timeout=3,
            sleep=1,
            exceptions_dict={ConflictError: []},
            func=self.update,
            resource_dict=resource,
        )
        self.logger.info(f"Applying {resource}")
        for _ in samples:
            return

    def deploy(self, wait=False):
        self.ipv4_ports_backup()
        self.ipv6_ports_backup()

        self.create(wait=wait)
        try:
            self.wait_for_status_success()
            return self
        except Exception as exp:
            self.logger.error(exp)
            super().__exit__(exception_type=None, exception_value=None, traceback=None)
            raise

    def clean_up(self):
        if self.teardown_absent_ifaces:
            try:
                self._absent_interface()
                self.wait_for_status_success()
            except Exception as exp:
                self.logger.error(exp)

        super().clean_up()

    def _absent_interface(self):
        for _iface in self.desired_state["interfaces"]:
            _iface["state"] = self.Interface.State.ABSENT
            self.set_interface(interface=_iface)

        if self.ports:
            self.add_ports()

        ResourceEditor(
            patches={
                self: {
                    "spec": {
                        "desiredState": {"interfaces": self.desired_state["interfaces"]}
                    }
                }
            }
        ).update()

    @property
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
                    or sample[0]["reason"]
                    == self.Conditions.Reason.CONFIGURATION_PROGRESSING
                )
            ):
                return sample

    def _process_failed_status(self, failed_condition_reason):
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

    def wait_for_status_success(self):
        failed_condition_reason = self.Conditions.Reason.FAILED_TO_CONFIGURE
        no_match_node_condition_reason = self.Conditions.Reason.NO_MATCHING_NODE

        # if we get here too fast there are no conditions, we need to wait.
        self.wait_for_configuration_conditions_unknown_or_progressing()

        samples = TimeoutSampler(
            wait_timeout=self.success_timeout, sleep=1, func=lambda: self.status
        )
        try:
            for sample in samples:
                if sample == self.Conditions.Reason.SUCCESSFULLY_CONFIGURED:
                    self.logger.info(f"NNCP {self.name} configured Successfully")
                    return sample

                elif sample == no_match_node_condition_reason:
                    raise NNCPConfigurationFailed(
                        f"{self.name}. Reason: {no_match_node_condition_reason}"
                    )

                elif sample == failed_condition_reason:
                    self._process_failed_status(
                        failed_condition_reason=failed_condition_reason
                    )

        except (TimeoutExpiredError, NNCPConfigurationFailed):
            self.logger.error(
                f"Unable to configure NNCP {self.name} "
                f"{f'nodes: {[node.name for node in self.nodes]}' if self.nodes else ''}"
            )
            raise

    @property
    def nnces(self):
        nnces = []
        for nnce in NodeNetworkConfigurationEnactment.get(dyn_client=self.client):
            if nnce.name.endswith(f".{self.name}"):
                nnces.append(nnce)
        return nnces

    def node_nnce(self, node_name):
        nnce = [
            nnce for nnce in self.nnces if nnce.labels["nmstate.io/node"] == node_name
        ]
        return nnce[0] if nnce else None

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
            err_msg += f"{nnce_prefix}: {libnmstate_err[0]}"

        return err_msg

    def _get_failed_nnce(self):
        for nnce in self.nnces:
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
