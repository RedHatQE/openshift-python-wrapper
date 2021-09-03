# -*- coding: utf-8 -*-

from ocp_resources.resource import NamespacedResource


class RoleBinding(NamespacedResource):
    """
    RoleBinding object
    """

    api_group = NamespacedResource.ApiGroup.RBAC_AUTHORIZATION_K8S_IO

    def __init__(
        self,
        name=None,
        namespace=None,
        client=None,
        subjects_kind=None,
        subjects_name=None,
        subjects_namespace=None,
        subjects_api_group=None,
        role_ref_kind=None,
        role_ref_name=None,
        teardown=True,
        yaml_file=None,
    ):

        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            teardown=teardown,
            yaml_file=yaml_file,
        )
        self.subjects_kind = subjects_kind
        self.subjects_name = subjects_name
        self.subjects_namespace = subjects_namespace
        self.subjects_api_group = subjects_api_group
        self.role_ref_kind = role_ref_kind
        self.role_ref_name = role_ref_name

    def to_dict(self):
        res = super().to_dict()
        if self.yaml_file:
            return res

        subjects = {}
        if self.subjects_kind:
            subjects["kind"] = self.subjects_kind
        if self.subjects_name:
            subjects["name"] = self.subjects_name
        if self.subjects_namespace:
            subjects["namespace"] = self.subjects_namespace
        if self.subjects_api_group:
            subjects["apiGroup"] = self.subjects_api_group
        if subjects:
            res["subjects"] = [subjects]

        roleref = {}
        if self.role_ref_kind:
            roleref["kind"] = self.role_ref_kind
        if self.role_ref_name:
            roleref["name"] = self.role_ref_name
        if roleref:
            roleref["apiGroup"] = self.api_group
            res["roleRef"] = roleref
        return res
