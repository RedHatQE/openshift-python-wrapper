from .resource import NamespacedResource


class Secret(NamespacedResource):
    """
    Secret object.
    """

    api_version = "v1"

    def __init__(
        self,
        name,
        namespace,
        accesskeyid=None,
        secretkey=None,
        htpasswd=None,
        teardown=True,
        data_dict=None,
        string_data=None,
    ):
        super().__init__(name=name, namespace=namespace, teardown=teardown)
        self.accesskeyid = accesskeyid
        self.secretkey = secretkey
        self.htpasswd = htpasswd
        self.data_dict = data_dict
        self.string_data = string_data

    def to_dict(self):
        res = super()._base_body()
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
