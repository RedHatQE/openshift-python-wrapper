# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.resource import NamespacedResource


class MLflowConfig(NamespacedResource):
    """
        MLflowConfig is a namespace-scoped configuration resource that allows
    Kubernetes namespace owners to override the default artifact storage
    for their namespace.
    """

    api_group: str = NamespacedResource.ApiGroup.MLFLOW_KUBEFLOW_ORG

    def __init__(
        self,
        artifact_root_path: str | None = None,
        artifact_root_secret: str | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            artifact_root_path (str): ArtifactRootPath is an optional relative path from the bucket root
              specified in the ArtifactRootSecret. When provided, this path is
              appended to the bucket URI from the secret to form the resolved
              artifact root.  Example:   artifactRootSecret: "mlflow-artifact-
              connection"  # Contains bucket: ds-team-bucket   artifactRootPath:
              "experiments"   resolved artifact root: s3://ds-team-
              bucket/experiments

            artifact_root_secret (str): ArtifactRootSecret is the name of a Secret in this namespace that
              contains credentials and bucket information for accessing the
              artifact storage.  The Secret must have the required keys for s3
              compatible storage: Example Secret:   apiVersion: v1   kind:
              Secret   metadata:     name: mlflow-artifact-connection
              namespace: ds-team-namespace   data:     AWS_ACCESS_KEY_ID:
              <base64-encoded>     AWS_SECRET_ACCESS_KEY: <base64-encoded>
              AWS_S3_BUCKET: <base64-encoded>     AWS_S3_ENDPOINT:
              <base64-encoded>     AWS_DEFAULT_REGION: <base64-encoded>  #
              Optional (default region is not always required, e.g. minio)

        """
        super().__init__(**kwargs)

        self.artifact_root_path = artifact_root_path
        self.artifact_root_secret = artifact_root_secret

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.artifact_root_secret is None:
                raise MissingRequiredArgumentError(argument="self.artifact_root_secret")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["artifactRootSecret"] = self.artifact_root_secret

            if self.artifact_root_path is not None:
                _spec["artifactRootPath"] = self.artifact_root_path

    # End of generated code
