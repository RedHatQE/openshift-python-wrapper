import json

from ocp_resources.resource import MissingRequiredArgumentError, NamespacedResource

DEFAULT_CNI_VERSION = "0.3.1"


class NetworkAttachmentDefinition(NamespacedResource):
    """
    NetworkAttachmentDefinition object.
    """

    api_group = NamespacedResource.ApiGroup.K8S_CNI_CNCF_IO
    resource_name = None

    def __init__(
        self,
        name=None,
        namespace=None,
        client=None,
        cni_type=None,
        cni_version=DEFAULT_CNI_VERSION,
        config=None,
        *args,
        **kwargs,
    ):
        """
        Create and manage NetworkAttachmentDefinition

        Args:
            name (str): Name of the NetworkAttachmentDefinition.
            namespace (str): Namespace of the NetworkAttachmentDefinition
            client: (DynamicClient): DynamicClient to use.
            cni_type (str): NetworkAttachmentDefinition CNI.
            cni_version (str): NetworkAttachmentDefinition CNI version.
            config (dict): NetworkAttachmentDefinition spec["config"] to use,
                if config is None basic config will be created.
        """
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            *args,
            **kwargs,
        )
        self.cni_type = cni_type
        self.cni_version = cni_version
        self.config = config

    def to_dict(self) -> None:
        super().to_dict()
        if not self.kind_dict and not self.yaml_file:
            if self.resource_name is not None:
                self.res["metadata"]["annotations"] = {
                    f"{NamespacedResource.ApiGroup.K8S_V1_CNI_CNCF_IO}/resourceName": (self.resource_name)
                }
            self.res["spec"] = {}
            if self.config:
                self.res["spec"]["config"] = self.config
            else:
                self.res["spec"]["config"] = {
                    "cniVersion": self.cni_version,
                    "type": self.cni_type,
                }


class BridgeNetworkAttachmentDefinition(NetworkAttachmentDefinition):
    def __init__(
        self,
        name,
        namespace,
        bridge_name,
        cni_type,
        cni_version=DEFAULT_CNI_VERSION,
        vlan=None,
        client=None,
        mtu=None,
        macspoofchk=None,
        teardown=True,
        old_nad_format=False,
        add_resource_name=True,
        dry_run=None,
    ):
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            teardown=teardown,
            dry_run=dry_run,
            cni_version=cni_version,
            cni_type=cni_type,
        )
        self.old_nad_format = old_nad_format
        self.bridge_name = bridge_name
        self.vlan = vlan
        self.mtu = mtu
        self.macspoofchk = macspoofchk
        self.add_resource_name = add_resource_name

    def to_dict(self) -> None:
        super().to_dict()
        spec_config = self.res["spec"]["config"]
        spec_config["name"] = self.bridge_name
        spec_config["bridge"] = self.bridge_name

        if self.mtu:
            spec_config["mtu"] = self.mtu

        if self.vlan:
            spec_config["vlan"] = self.vlan

        if self.macspoofchk:
            spec_config["macspoofchk"] = self.macspoofchk

        self.res["spec"]["config"] = spec_config


class LinuxBridgeNetworkAttachmentDefinition(BridgeNetworkAttachmentDefinition):
    def __init__(
        self,
        name,
        namespace,
        bridge_name,
        cni_type="cnv-bridge",
        cni_version=DEFAULT_CNI_VERSION,
        vlan=None,
        client=None,
        mtu=None,
        tuning_type=None,
        teardown=True,
        macspoofchk=None,
        add_resource_name=True,
        dry_run=None,
    ):
        super().__init__(
            name=name,
            namespace=namespace,
            bridge_name=bridge_name,
            cni_type=cni_type,
            vlan=vlan,
            client=client,
            mtu=mtu,
            teardown=teardown,
            macspoofchk=macspoofchk,
            add_resource_name=add_resource_name,
            dry_run=dry_run,
            cni_version=cni_version,
        )
        self.tuning_type = tuning_type

    def to_dict(self) -> None:
        super().to_dict()
        if self.tuning_type:
            self.old_nad_format = True
            self.res["spec"]["config"].setdefault("plugins", []).append({"type": self.tuning_type})

        self.res["spec"]["config"] = json.dumps(self.res["spec"]["config"])

    @property
    def resource_name(self):
        if self.add_resource_name:
            return f"bridge.network.kubevirt.io/{self.bridge_name}"


class OvsBridgeNetworkAttachmentDefinition(BridgeNetworkAttachmentDefinition):
    def __init__(
        self,
        name,
        namespace,
        bridge_name,
        vlan=None,
        client=None,
        mtu=None,
        teardown=True,
        dry_run=None,
        cni_version=DEFAULT_CNI_VERSION,
    ):
        super().__init__(
            name=name,
            namespace=namespace,
            bridge_name=bridge_name,
            cni_type="ovs",
            vlan=vlan,
            client=client,
            mtu=mtu,
            teardown=teardown,
            dry_run=dry_run,
            cni_version=cni_version,
        )

    def to_dict(self) -> None:
        super().to_dict()
        self.res["spec"]["config"] = json.dumps(self.res["spec"]["config"])

    @property
    def resource_name(self):
        return f"ovs-cni.network.kubevirt.io/{self.bridge_name}"


class OVNOverlayNetworkAttachmentDefinition(NetworkAttachmentDefinition):
    def __init__(
        self,
        network_name=None,
        topology=None,
        vlan=None,
        mtu=None,
        **kwargs,
    ):
        """
        Create and manage an OVN k8s overlay NetworkAttachmentDefinition (a switched, layer 2, topology network).

        API reference:
        https://docs.openshift.com/container-platform/4.14/networking/multiple_networks/configuring-additional-network.html#configuration-ovnk-additional-networks_configuring-additional-network

        Args:
            network_name (str, optional): The name of the network, used to connect
                resources created in different namespaces to the same network.
            vlan (int, optional): A vlan tag ID that will be assigned to traffic from this
                additional network.
            mtu (str, optional): The maximum transmission unit (MTU).
            topology (str): The secondary network topology to be created.
        """
        super().__init__(
            cni_type="ovn-k8s-cni-overlay",
            **kwargs,
        )
        self.network_name = network_name
        self.topology = topology
        self.vlan = vlan
        self.mtu = mtu

    def to_dict(self) -> None:
        super().to_dict()
        if not self.kind_dict and not self.yaml_file:
            if not self.network_name and not self.topology:
                raise MissingRequiredArgumentError(argument="'network_name' and 'topology'")

            spec_config = self.res["spec"]["config"]
            if self.vlan:
                spec_config["vlanID"] = self.vlan
            if self.mtu:
                spec_config["mtu"] = self.mtu
            spec_config["name"] = self.network_name
            spec_config["topology"] = self.topology
            spec_config["netAttachDefName"] = f"{self.namespace}/{self.name}"
            self.res["spec"]["config"] = json.dumps(spec_config)
