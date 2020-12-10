# -*- coding: utf-8 -*-

from .resource import Resource


class ClusterRoleBinding(Resource):
    """
    ClusterRoleBinding object.
    """

    api_group = Resource.ApiGroup.RBAC_AUTHORIZATION_K8S_IO

    def __init__(
        self, name, client=None, teardown=True,
    ):
        super().__init__(name=name, client=client, teardown=teardown)
