# -*- coding: utf-8 -*-
from ocp_resources.resource import Resource


class ClusterRole(Resource):
    """
    ClusterRole object
    'rbac_authorization_k8s_io' API official docs:
        https://docs.openshift.com/container-platform/3.11/rest_api/rbac_authorization_k8s_io/rbac-authorization-k8s-io-index.html
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

    def to_dict(self):
        if not self.yaml_file:
            if not self.rules and not self.yaml_file:
                raise ValueError("must send rules or yaml_file")
            if not self.res:
                super().to_dict()
            self.res["rules"] = self.rules
