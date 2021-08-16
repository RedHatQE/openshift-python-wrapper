# -*- coding: utf-8 -*-

from ocp_resources.resource import NamespacedResource


class ServiceMeshMemberRoll(NamespacedResource):
    """
    Service Mesh Member Roll object.
    """

    api_version = NamespacedResource.ApiGroup.MAISTRA_IO

    class Status:
        CONFIGURED = "Configured"
