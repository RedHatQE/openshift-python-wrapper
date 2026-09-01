# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md


from typing import Any

from ocp_resources.resource import NamespacedResource


class FileRestoreOperator(NamespacedResource):
    """
    FileRestoreOperator is the Schema for the filerestoreoperators API
    """

    api_group: str = NamespacedResource.ApiGroup.FILERESTORE_KUBEVIRT_IO

    def __init__(
        self,
        image_pull_policy: str | None = None,
        tls_security_profile: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            image_pull_policy (str): ImagePullPolicy describes a policy for if/when to pull container
              images

            tls_security_profile (dict[str, Any]): TLSSecurityProfile configures TLS settings for metrics server

        """
        super().__init__(**kwargs)

        self.image_pull_policy = image_pull_policy
        self.tls_security_profile = tls_security_profile

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.image_pull_policy is not None:
                _spec["imagePullPolicy"] = self.image_pull_policy

            if self.tls_security_profile is not None:
                _spec["tlsSecurityProfile"] = self.tls_security_profile

    # End of generated code
