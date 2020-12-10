# -*- coding: utf-8 -*-

from .resource import NamespacedResource


class Role(NamespacedResource):
    """
    Role object.
    """

    api_group = NamespacedResource.ApiGroup.RBAC_AUTHORIZATION_K8S_IO

    def __init__(
        self,
        name,
        namespace,
        client=None,
        teardown=True,
    ):
        super().__init__(
            name=name, namespace=namespace, client=client, teardown=teardown
        )
