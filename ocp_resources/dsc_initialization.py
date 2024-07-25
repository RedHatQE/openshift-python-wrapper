# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, Optional
from ocp_resources.resource import NamespacedResource


class DSCInitialization(NamespacedResource):
    """
    DSCInitialization is the Schema for the dscinitializations API.

    API Link: https://github.com/opendatahub-io/opendatahub-operator/blob/incubation/apis/dscinitialization/v1/dscinitialization_types.go
    """

    api_version: str = "dscinitialization.opendatahub.io/v1"

    def __init__(
        self,
        applications_namespace: Optional[str] = "",
        dev_flags: Optional[Dict[str, Any]] = None,
        monitoring: Optional[Dict[str, Any]] = None,
        service_mesh: Optional[Dict[str, Any]] = None,
        trusted_cabundle: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            applications_namespace(str): Namespace for applications to be installed.
            dev_flags(Dict[Any, Any]): Internal development field to test customizations.
            monitoring(Dict[Any, Any]): Enable monitoring on specified namespace.
            service_mesh(Dict[Any, Any]): Configures Service Mesh as networking layer for Data Science Clusters components.
            trusted_cabundle(Dict[Any, Any]): Configures TrustedCABundle ConfigMap.
        """
        super().__init__(**kwargs)

        self.applications_namespace = applications_namespace
        self.dev_flags = dev_flags
        self.monitoring = monitoring
        self.service_mesh = service_mesh
        self.trusted_cabundle = trusted_cabundle

    def to_dict(self) -> None:
        super().to_dict()

        if not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.applications_namespace:
                self.res["applicationsNamespace"] = self.applications_namespace

            if self.dev_flags:
                self.res["devFlags"] = self.dev_flags

            if self.monitoring:
                self.res["monitoring"] = self.monitoring

            if self.service_mesh:
                self.res["serviceMesh"] = self.service_mesh

            if self.trusted_cabundle:
                self.res["trustedCABundle"] = self.trusted_cabundle
