# -*- coding: utf-8 -*-

from resources.resource import Resource


class HostPathProvisioner(Resource):
    """
    HostPathProvisioner Custom Resource Object.
    """

    api_group = Resource.ApiGroup.HOSTPATHPROVISIONER_KUBEVIRT_IO

    class Name:
        HOSTPATH_PROVISIONER = "hostpath-provisioner"

    def __init__(
        self,
        name,
        client=None,
        teardown=True,
    ):
        super().__init__(name=name, client=client, teardown=teardown)

    @property
    def volume_path(self):
        return self.instance.spec.pathConfig.path
