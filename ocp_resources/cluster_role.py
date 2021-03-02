# -*- coding: utf-8 -*-

from ocp_resources.resource import Resource


class ClusterRole(Resource):
    """
    ClusterRole object
    """

    api_group = Resource.ApiGroup.RBAC_AUTHORIZATION_K8S_IO

    def __init__(
        self,
        name,
        client=None,
        api_groups=None,
        permissions_to_resources=None,
        verbs=None,
        teardown=True,
    ):
        super().__init__(client=client, name=name, teardown=teardown)
        self.api_groups = api_groups
        self.permissions_to_resources = permissions_to_resources
        self.verbs = verbs

    def to_dict(self):
        res = super().to_dict()
        rules = {}
        if self.api_groups:
            rules["apiGroups"] = self.api_groups
        if self.permissions_to_resources:
            rules["resources"] = self.permissions_to_resources
        if self.verbs:
            rules["verbs"] = self.verbs
        if rules:
            res["rules"] = [rules]
        return res
