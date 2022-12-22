# -*- coding: utf-8 -*-
from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.resource import Resource


class ClusterRole(Resource):
    """
    ClusterRole object
    """

    api_group = Resource.ApiGroup.RBAC_AUTHORIZATION_K8S_IO

    def __init__(
        self,
        name=None,
        client=None,
        rules=None,
        teardown=True,
        yaml_file=None,
        delete_timeout=TIMEOUT_4MINUTES,
        **kwargs,
    ):
        """
        Args:
            name (str): Role name.
            client (DynamicClient): DynamicClient to use.
            rules (list): list of dicts of rules. In the dict:
                permissions_to_resources (list): List of string with resource/s to which you want to add permissions to.
                Verbs (list): Determine the action/s (permissions) applicable on a specific resource.
                    Available verbs per resource can be seen with the command 'oc api-resources --sort-by name -o wide'
            teardown (bool, default: True): Indicates if this resource would need to be deleted.
            yaml_file (yaml, default: None): yaml file for the resource.
            delete_timeout (int, default: 4 minutes): timeout associated with delete action.
        """
        super().__init__(
            client=client,
            name=name,
            teardown=teardown,
            yaml_file=yaml_file,
            delete_timeout=delete_timeout,
            **kwargs,
        )
        self.rules = rules

    def to_dict(self):
        if not self.rules and not self.yaml_file:
            raise ValueError("must send rules or yaml_file")
        if not self.res:
            super().to_dict()
        if not self.yaml_file:
            self.res["rules"] = self.rules
