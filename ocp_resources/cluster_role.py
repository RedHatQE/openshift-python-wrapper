# -*- coding: utf-8 -*-
from ocp_resources.resource import MissingRequiredArgumentError, Resource


class ClusterRole(Resource):
    """
    https://kubernetes.io/docs/reference/kubernetes-api/authorization-resources/cluster-role-v1/
    """

    api_group = Resource.ApiGroup.RBAC_AUTHORIZATION_K8S_IO

    def __init__(self, rules=None, **kwargs):
        """
        Args:
            rules (list): list of dicts of rules. In the dict:
                permissions_to_resources (list): List of string with resource/s to which you want to add permissions to.
                Verbs (list): Determine the action/s (permissions) applicable on a specific resource.
                    Available verbs per resource can be seen with the command 'oc api-resources --sort-by name -o wide'
        """
        super().__init__(**kwargs)
        self.rules = rules

    def to_dict(self) -> None:
        super().to_dict()
        if not self.yaml_file:
            if not self.rules:
                raise MissingRequiredArgumentError(argument="rules")
            self.res["rules"] = self.rules
