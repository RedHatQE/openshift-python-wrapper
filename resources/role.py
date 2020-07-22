# -*- coding: utf-8 -*-

from .resource import NamespacedResource


class Role(NamespacedResource):
    """
    Role object.
    """

    api_group = "rbac.authorization.k8s.io"
