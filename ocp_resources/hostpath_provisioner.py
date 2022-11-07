# -*- coding: utf-8 -*-
from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.resource import Resource


class HostPathProvisioner(Resource):
    """
    HostPathProvisioner Custom Resource Object.
    """

    api_group = Resource.ApiGroup.HOSTPATHPROVISIONER_KUBEVIRT_IO

    class Name:
        HOSTPATH_PROVISIONER = "hostpath-provisioner"

    def __init__(
        self,
        name=None,
        path=None,
        image_pull_policy=None,
        client=None,
        teardown=True,
        yaml_file=None,
        delete_timeout=TIMEOUT_4MINUTES,
        **kwargs,
    ):
        super().__init__(
            name=name,
            client=client,
            teardown=teardown,
            yaml_file=yaml_file,
            delete_timeout=delete_timeout,
            **kwargs,
        )
        self.path = path
        self.image_pull_policy = image_pull_policy

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file:
            spec = self.res.setdefault("spec", {})
            path_config = spec.setdefault("pathConfig", {})
            if self.path:
                path_config["path"] = self.path
            if self.image_pull_policy:
                spec["imagePullPolicy"] = self.image_pull_policy

    @property
    def volume_path(self):
        return self.instance.spec.pathConfig.path
