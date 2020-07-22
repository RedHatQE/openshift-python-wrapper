# -*- coding: utf-8 -*-

from .resource import Resource


class ClusterRoleBinding(Resource):
    """
    ClusterRoleBinding object.
    """

    api_group = "rbac.authorization.k8s.io"
