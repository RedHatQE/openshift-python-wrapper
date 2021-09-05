# -*- coding: utf-8 -*-

from ocp_resources.resource import NamespacedResource


class ServiceMeshMemberRoll(NamespacedResource):
    """
    Service Mesh Control Plane object.
    """

    api_group = NamespacedResource.ApiGroup.MAISTRA_IO
