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
        api_groups=None,
        permissions_to_resources=None,
        verbs=None,
        teardown=True,
        yaml_file=None,
        delete_timeout=TIMEOUT_4MINUTES,
        **kwargs,
    ):
        super().__init__(
            client=client,
            name=name,
            teardown=teardown,
            yaml_file=yaml_file,
            delete_timeout=delete_timeout,
            **kwargs,
        )
        self.api_groups = api_groups
        self.permissions_to_resources = permissions_to_resources
        self.verbs = verbs
        self.desired_state = {"rules": []}

    def to_dict(self):
        self.res = super().to_dict()
        if self.yaml_file:
            return self.res

        if self.permissions_to_resources:
            self.add_rule(
                api_groups=self.api_groups,
                permissions_to_resources=self.permissions_to_resources,
                verbs=self.verbs,
            )

        return self.res

    def add_rule(
        self,
        api_groups=None,
        permissions_to_resources=None,
        verbs=None,
    ):
        if not self.res:
            self.res = super().to_dict()

        rule = {}
        if api_groups:
            rule["apiGroups"] = api_groups
        if permissions_to_resources:
            rule["resources"] = permissions_to_resources
        if verbs:
            rule["verbs"] = verbs
        if rule:
            self._set_rule(rule=rule)

        return self.res

    def _set_rule(self, rule):

        self.desired_state["rules"].append(rule)
        self.res["rules"] = self.desired_state["rules"]
