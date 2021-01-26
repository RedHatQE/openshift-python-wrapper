# -*- coding: utf-8 -*-

from resources.resource import NamespacedResource


class ReplicaSet(NamespacedResource):
    """
    OpenShift Service object.
    """

    api_version = NamespacedResource.ApiVersion.V1
