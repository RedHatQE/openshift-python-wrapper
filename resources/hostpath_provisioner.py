# -*- coding: utf-8 -*-

from resources.resource import Resource


class HostPathProvisioner(Resource):
    """
    HostPathProvisioner Custom Resource Object.
    """

    api_group = "hostpathprovisioner.kubevirt.io"

    class Name:
        HOSTPATH_PROVISIONER = "hostpath-provisioner"

    @property
    def volume_path(self):
        return self.instance.spec.pathConfig.path
