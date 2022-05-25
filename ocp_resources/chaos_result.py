# -*- coding: utf-8 -*-

from ocp_resources.resource import NamespacedResource


class ChaosResult(NamespacedResource):
    """
    Litmus ChaosResult resource.
    """

    api_group = NamespacedResource.ApiGroup.LITMUS_IO
