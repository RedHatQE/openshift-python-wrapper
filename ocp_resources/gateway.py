# -*- coding: utf-8 -*-

from ocp_resources.resource import NamespacedResource


class Gateway(NamespacedResource):
    """
    Gateway object.
    """

    api_group = NamespacedResource.ApiGroup.NETWORKING_ISTIO_IO
