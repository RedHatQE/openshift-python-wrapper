# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import MissingRequiredArgumentError, Resource


class DSCInitialization(Resource):
    """
    DSCInitialization is the Schema for the dscinitializations API.
    """

    api_group: str = Resource.ApiGroup.DSCINITIALIZATION_OPENDATAHUB_IO

    def __init__(
        self,
        applications_namespace: str | None = None,
        dev_flags: dict[str, Any] | None = None,
        monitoring: dict[str, Any] | None = None,
        service_mesh: dict[str, Any] | None = None,
        trusted_ca_bundle: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            applications_namespace (str): Namespace for applications to be installed, non-configurable, default
              to "redhat-ods-applications"

            dev_flags (dict[str, Any]): Internal development useful field to test customizations. This is not
              recommended to be used in production environment.

            monitoring (dict[str, Any]): Enable monitoring on specified namespace

            service_mesh (dict[str, Any]): Configures Service Mesh as networking layer for Data Science Clusters
              components. The Service Mesh is a mandatory prerequisite for
              single model serving (KServe) and you should review this
              configuration if you are planning to use KServe. For other
              components, it enhances user experience; e.g. it provides unified
              authentication giving a Single Sign On experience.

            trusted_ca_bundle (dict[str, Any]): When set to `Managed`, adds odh-trusted-ca-bundle Configmap to all
              namespaces that includes cluster-wide Trusted CA Bundle in
              .data["ca-bundle.crt"]. Additionally, this fields allows admins to
              add custom CA bundles to the configmap using the .CustomCABundle
              field.

        """
        super().__init__(**kwargs)

        self.applications_namespace = applications_namespace
        self.dev_flags = dev_flags
        self.monitoring = monitoring
        self.service_mesh = service_mesh
        self.trusted_ca_bundle = trusted_ca_bundle

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.applications_namespace is None:
                raise MissingRequiredArgumentError(argument="self.applications_namespace")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["applicationsNamespace"] = self.applications_namespace

            if self.dev_flags is not None:
                _spec["devFlags"] = self.dev_flags

            if self.monitoring is not None:
                _spec["monitoring"] = self.monitoring

            if self.service_mesh is not None:
                _spec["serviceMesh"] = self.service_mesh

            if self.trusted_ca_bundle is not None:
                _spec["trustedCABundle"] = self.trusted_ca_bundle

    # End of generated code
