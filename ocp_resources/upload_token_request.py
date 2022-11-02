# -*- coding: utf-8 -*-

from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.resource import NamespacedResource


class UploadTokenRequest(NamespacedResource):
    """
    OpenShift UploadTokenRequest object.
    """

    api_group = NamespacedResource.ApiGroup.UPLOAD_CDI_KUBEVIRT_IO

    def __init__(
        self,
        name=None,
        namespace=None,
        client=None,
        pvc_name=None,
        teardown=True,
        yaml_file=None,
        delete_timeout=TIMEOUT_4MINUTES,
        **kwargs,
    ):
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            teardown=teardown,
            yaml_file=yaml_file,
            delete_timeout=delete_timeout,
            **kwargs,
        )
        self.pvc_name = pvc_name

    def to_dict(self):
        res = super().to_dict()
        if self.yaml_file:
            return res

        res.update({"spec": {"pvcName": self.pvc_name}})
        return res
