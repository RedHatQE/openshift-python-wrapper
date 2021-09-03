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
    ):
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            teardown=teardown,
            yaml_file=yaml_file,
        )
        self.accesskeyid = accesskeyid
        self.secretkey = secretkey
        self.htpasswd = htpasswd
        self.data_dict = data_dict
        self.string_data = string_data

    def to_dict(self):
        res = super().to_dict()
        if self.yaml_file:
            return res

        if self.accesskeyid:
            res.update(
                {"data": {"accessKeyId": self.accesskeyid, "secretKey": self.secretkey}}
            )
        if self.htpasswd:
            res.update({"data": {"htpasswd": self.htpasswd}})
        if self.data_dict:
            res.update({"data": self.data_dict})
        if self.string_data:
            res.update({"stringData": self.string_data})

        return res

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
