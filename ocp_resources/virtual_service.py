# -*- coding: utf-8 -*-

from ocp_resources.resource import NamespacedResource


class VirtualService(NamespacedResource):
    """
    Virtual Service object.
    """

    api_group = NamespacedResource.ApiGroup.NETWORKING_ISTIO_IO
