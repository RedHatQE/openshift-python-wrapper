# -*- coding: utf-8 -*-

from .resource import NamespacedResource


class Service(NamespacedResource):
    """
    OpenShift Service object.
    """

    api_version = "v1"
