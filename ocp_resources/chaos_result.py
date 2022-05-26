# -*- coding: utf-8 -*-

from ocp_resources.resource import NamespacedResource


class ChaosResult(NamespacedResource):
    """
    ChaosResult resource used in Litmus experiments.
    """

    api_group = NamespacedResource.ApiGroup.LITMUS_IO
