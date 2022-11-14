from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.resource import NamespacedResource


class Secret(NamespacedResource):
    """
    Secret object.
    """

    api_version = NamespacedResource.ApiVersion.V1

    def __init__(
        self,
        name=None,
        namespace=None,
        client=None,
        accesskeyid=None,
        secretkey=None,
        htpasswd=None,
        teardown=True,
        data_dict=None,
        string_data=None,
        yaml_file=None,
        delete_timeout=TIMEOUT_4MINUTES,
        type=None,
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
        self.accesskeyid = accesskeyid
        self.secretkey = secretkey
        self.htpasswd = htpasswd
        self.data_dict = data_dict
        self.string_data = string_data
        self.type = type

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file:
            if self.accesskeyid:
                self.res.update(
                    {
                        "data": {
                            "accessKeyId": self.accesskeyid,
                            "secretKey": self.secretkey,
                        }
                    }
                )
            if self.htpasswd:
                self.res.update({"data": {"htpasswd": self.htpasswd}})
            if self.data_dict:
                self.res.update({"data": self.data_dict})
            if self.string_data:
                self.res.update({"stringData": self.string_data})
            if self.type:
                self.res.update({"type": self.type})

    @property
    def certificate_not_after(self):
        return self.instance.metadata.annotations[
            "auth.openshift.io/certificate-not-after"
        ]

    @property
    def certificate_not_before(self):
        return self.instance.metadata.annotations[
            "auth.openshift.io/certificate-not-before"
        ]
