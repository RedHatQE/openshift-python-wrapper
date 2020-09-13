# -*- coding: utf-8 -*-

from .resource import NamespacedResource


class Role(NamespacedResource):
    """
    Role object.
    """

    api_group = NamespacedResource.ApiGroup.RBAC_AUTHORIZATION_K8S_IO
