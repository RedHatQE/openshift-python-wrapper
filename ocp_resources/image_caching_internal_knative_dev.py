# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, List, Optional
from ocp_resources.resource import NamespacedResource, MissingRequiredArgumentError


class Image(NamespacedResource):
    """
    Image is a Knative abstraction that encapsulates the interface by which Knative components express a desire to have a particular image cached.
    """

    api_group: str = NamespacedResource.ApiGroup.CACHING_INTERNAL_KNATIVE_DEV

    def __init__(
        self,
        image: Optional[str] = "",
        image_pull_secrets: Optional[List[Any]] = None,
        service_account_name: Optional[str] = "",
        **kwargs: Any,
    ) -> None:
        """
        Args:
            image (str): Image is the name of the container image url to cache across the
              cluster.

            image_pull_secrets (List[Any]): ImagePullSecrets contains the names of the Kubernetes Secrets
              containing login information used by the Pods which will run this
              container.

            service_account_name (str): ServiceAccountName is the name of the Kubernetes ServiceAccount as
              which the Pods will run this container.  This is potentially used
              to authenticate the image pull if the service account has attached
              pull secrets.  For more information:
              https://kubernetes.io/docs/tasks/configure-pod-
              container/configure-service-account/#add-imagepullsecrets-to-a-
              service-account

        """
        super().__init__(**kwargs)

        self.image = image
        self.image_pull_secrets = image_pull_secrets
        self.service_account_name = service_account_name

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if not self.image:
                raise MissingRequiredArgumentError(argument="self.image")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["image"] = self.image

            if self.image_pull_secrets:
                _spec["imagePullSecrets"] = self.image_pull_secrets

            if self.service_account_name:
                _spec["serviceAccountName"] = self.service_account_name

    # End of generated code
