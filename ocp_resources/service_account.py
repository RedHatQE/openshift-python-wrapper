import kubernetes
from ocp_resources.resource import NamespacedResource


class ServiceAccount(NamespacedResource):
    """
    https://kubernetes.io/docs/reference/kubernetes-api/authentication-resources/service-account-v1/
    """

    api_version = NamespacedResource.ApiVersion.V1

    def __init__(
        self,
        automount_service_account_token=None,
        image_pull_secrets=None,
        secrets=None,
        **kwargs,
    ):
        """
        Args:
            automount_service_account_token (bool, Optional): indicates whether pods running as this service account should have an
                                                 API token automatically mounted
            image_pull_secrets (list, Optional): list of references to secrets in the same namespace to use for pulling pod images
            secrets (list, Optional): list of secrets for the pods to use
        """
        super().__init__(**kwargs)
        self.automount_service_account_token = automount_service_account_token
        self.image_pull_secrets = image_pull_secrets
        self.secrets = secrets

    def to_dict(self) -> None:
        super().to_dict()
        if not self.yaml_file:
            if self.automount_service_account_token:
                self.res["automountServiceAccountToken"] = self.automount_service_account_token
            if self.image_pull_secrets:
                self.res["imagePullSecrets"] = self.image_pull_secrets
            if self.secrets:
                self.res["secrets"] = self.secrets

    def create_service_account_token(self, audiences=None, bound_object_ref=None, expiration_seconds=None):
        """
        Args:
            audiences (list, Optional): Intended audiences of the token
            bound_object_ref (dict, Optional): Reference to an object that a token is bound to
            expiration_seconds (int, Optional): Requested duration of validity of the token in seconds.
        """
        return self._kube_v1_api.create_namespaced_service_account_token(
            name=self.name,
            namespace=self.namespace,
            body=kubernetes.client.AuthenticationV1TokenRequest(
                spec={
                    "audiences": audiences,
                    "boundObjectRef": bound_object_ref,
                    "expirationSeconds": expiration_seconds,
                }
            ),
        )
