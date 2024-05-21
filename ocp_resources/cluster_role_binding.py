# -*- coding: utf-8 -*-

from ocp_resources.cluster_role import ClusterRole
from ocp_resources.resource import MissingRequiredArgumentError, Resource


class ClusterRoleBinding(Resource):
    """
    https://kubernetes.io/docs/reference/kubernetes-api/authorization-resources/cluster-role-binding-v1/
    """

    api_group = Resource.ApiGroup.RBAC_AUTHORIZATION_K8S_IO

    def __init__(
        self,
        cluster_role=None,
        subjects=None,
        **kwargs,
    ):
        """
        Args:
            cluster_role (str): Name of referenced ClusterRole
            subjects (list, optional): User subjects that are authorised to access the cluster role
        """
        super().__init__(**kwargs)
        self.cluster_role = cluster_role
        self.subjects = subjects

    def to_dict(self) -> None:
        super().to_dict()
        if not self.yaml_file:
            if not self.cluster_role:
                raise MissingRequiredArgumentError(argument="cluster_role")

            self.res.setdefault("roleRef", {})
            self.res["roleRef"] = {
                "apiGroup": self.api_group,
                "kind": ClusterRole.kind,
                "name": self.cluster_role,
            }

            if self.subjects:
                self.res.setdefault("subjects", self.subjects)
