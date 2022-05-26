# -*- coding: utf-8 -*-

from ocp_resources.resource import NamespacedResource


class ChaosResult(NamespacedResource):
    """
    ChaosResult resource (LitmusChaos)
    """

    api_group = NamespacedResource.ApiGroup.LITMUS_IO
