import json

from ocp_resources.resource import NamespacedResource


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
        bridge_name=None,
        cni_type=None,
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
        )
        self.old_nad_format = old_nad_format
        self.bridge_name = bridge_name
        self.cni_type = cni_type
        self.vlan = vlan
        self.mtu = mtu
        self.macspoofchk = macspoofchk
        self.add_resource_name = add_resource_name

    def to_dict(self):
        res = super().to_dict()
        if self.yaml_file:
            return res

        res["spec"] = {}
        if self.resource_name is not None:
            res["metadata"]["annotations"] = {
                f"{NamespacedResource.ApiGroup.K8S_V1_CNI_CNCF_IO}/resourceName": self.resource_name
            }

        spec_config = {"cniVersion": "0.3.1", "name": self.bridge_name}
        bridge_dict = {"type": self.cni_type, "bridge": self.bridge_name}
        if self.mtu:
            bridge_dict["mtu"] = self.mtu
        if self.vlan:
            bridge_dict["vlan"] = self.vlan
        if self.old_nad_format:
            spec_config["plugins"] = [bridge_dict]
        else:
            spec_config.update(bridge_dict)
        if self.macspoofchk:
            spec_config["macspoofchk"] = self.macspoofchk

        res["spec"]["config"] = spec_config
        return res

    def wait_for_status(
        self, status, timeout=None, label_selector=None, resource_version=None
    ):
        raise NotImplementedError(f"{self.kind} does not have status")


class LinuxBridgeNetworkAttachmentDefinition(NetworkAttachmentDefinition):
    def __init__(
        self,
        name,
        namespace,
        bridge_name,
        cni_type="cnv-bridge",
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
        )
        self.tuning_type = tuning_type

    def to_dict(self):
        res = super().to_dict()
        if self.tuning_type:
            self.old_nad_format = True
            res["spec"]["config"].setdefault("plugins", []).append(
                {"type": self.tuning_type}
            )

        res["spec"]["config"] = json.dumps(res["spec"]["config"])
        return res

    @property
    def resource_name(self):
        if self.add_resource_name:
            return f"bridge.network.kubevirt.io/{self.bridge_name}"


class OvsBridgeNetworkAttachmentDefinition(NetworkAttachmentDefinition):
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
        )

    def to_dict(self):
        res = super().to_dict()
        res["spec"]["config"] = json.dumps(res["spec"]["config"])
        return res

    @property
    def resource_name(self):
        return f"ovs-cni.network.kubevirt.io/{self.bridge_name}"
