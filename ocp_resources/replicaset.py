# -*- coding: utf-8 -*-

from ocp_resources.resource import NamespacedResource


class ReplicaSet(NamespacedResource):
    """
    OpenShift Service object.
    """

    api_group = NamespacedResource.ApiGroup.APPS
