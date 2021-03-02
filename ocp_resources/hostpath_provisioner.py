# -*- coding: utf-8 -*-

from ocp_resources.resource import Resource


class HostPathProvisioner(Resource):
    """
    HostPathProvisioner Custom Resource Object.
    """

    api_group = Resource.ApiGroup.HOSTPATHPROVISIONER_KUBEVIRT_IO

    class Name:
        HOSTPATH_PROVISIONER = "hostpath-provisioner"

    @property
    def volume_path(self):
        return self.instance.spec.pathConfig.path
