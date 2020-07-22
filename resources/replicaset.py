# -*- coding: utf-8 -*-

from .resource import NamespacedResource


class ReplicaSet(NamespacedResource):
    """
    OpenShift Service object.
    """

    api_version = "v1"
