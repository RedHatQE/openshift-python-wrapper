from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.resource import NamespacedResource


class OCSInitialization(NamespacedResource):
    api_group = NamespacedResource.ApiGroup.OCS_OPENSHIFT_IO

    def __init__(
        self,
        name=None,
        namespace=None,
        client=None,
        teardown=False,
        privileged_client=None,
        yaml_file=None,
        delete_timeout=TIMEOUT_4MINUTES,
        enable_ceph_tools=None,
        **kwargs,
    ):
        """
        OCSInitialization object.
        API reference (source code linked here due to lack of API doc for this resource):
            https://github.com/red-hat-storage/ocs-operator/blob/main/api/v1/ocsinitialization_types.go

        Args:
            enable_ceph_tools (bool): When True, creates a Deployment named "rook-ceph-tools" in the "openshift-storage"
             namespace. More information about the Rook Ceph Toolbox can be found here:
             https://rook.io/docs/rook/v1.10/Troubleshooting/ceph-toolbox/
        """

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
        self.enable_ceph_tools = enable_ceph_tools

    def to_dict(self) -> None:
        super().to_dict()
        if not self.yaml_file and self.enable_ceph_tools is not None:
            self.res.update({
                "spec": {
                    "enableCephTools": self.enable_ceph_tools,
                }
            })
