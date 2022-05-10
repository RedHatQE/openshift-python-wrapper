# -*- coding: utf-8 -*-

from ocp_resources.cluster_role import ClusterRole
from ocp_resources.resource import Resource


class ClusterRoleBinding(Resource):
    """
    ClusterRoleBinding object.
    """

    api_group = Resource.ApiGroup.RBAC_AUTHORIZATION_K8S_IO

    def __init__(
        self,
        name=None,
        cluster_role=None,
        subjects=None,
    ):
        super().__init__(name=name)
        self.cluster_role = cluster_role
        self.subjects = subjects

    def to_dict(self):
        self.res = super().to_dict()

        self.res.setdefault("roleRef", {})
        self.res["roleRef"] = {
            "apiGroup": self.api_group,
            "kind": ClusterRole.kind,
            "name": self.cluster_role,
        }

        if self.subjects:
            self.res.setdefault("subjects", self.subjects)

        return self.res
