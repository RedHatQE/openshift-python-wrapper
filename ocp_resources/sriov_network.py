from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.resource import NamespacedResource


class SriovNetwork(NamespacedResource):
    """
    SriovNetwork object.
    """

    api_group = NamespacedResource.ApiGroup.SRIOVNETWORK_OPENSHIFT_IO

    def __init__(
        self,
        name=None,
        namespace=None,
        network_namespace=None,
        client=None,
        resource_name=None,
        vlan=None,
        ipam=None,
        teardown=True,
        yaml_file=None,
        delete_timeout=TIMEOUT_4MINUTES,
        macspoofchk=None,
        **kwargs,
    ):
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            teardown=teardown,
            yaml_file=yaml_file,
            delete_timeout=delete_timeout,
            **kwargs,
        )
        self.network_namespace = network_namespace
        self.resource_name = resource_name
        self.vlan = vlan
        self.ipam = ipam
        self.macspoofchk = macspoofchk

    def to_dict(self) -> None:
        super().to_dict()
        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {
                "ipam": self.ipam or "{}\n",
                "networkNamespace": self.network_namespace,
                "resourceName": self.resource_name,
            }
            if self.vlan:
                self.res["spec"]["vlan"] = self.vlan

            if self.macspoofchk:
                self.res["spec"]["spoofChk"] = self.macspoofchk
