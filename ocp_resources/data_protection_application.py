# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.resource import NamespacedResource


class DataProtectionApplication(NamespacedResource):
    """
    DataProtectionApplication is the Schema for the dpa API
    """

    api_group: str = NamespacedResource.ApiGroup.OADP_OPENSHIFT_IO

    def __init__(
        self,
        backup_images: bool | None = None,
        backup_locations: list[Any] | None = None,
        configuration: dict[str, Any] | None = None,
        features: dict[str, Any] | None = None,
        image_pull_policy: str | None = None,
        pod_annotations: dict[str, Any] | None = None,
        pod_dns_config: dict[str, Any] | None = None,
        pod_dns_policy: str | None = None,
        snapshot_locations: list[Any] | None = None,
        unsupported_overrides: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            backup_images (bool): backupImages is used to specify whether you want to deploy a registry
              for enabling backup and restore of images

            backup_locations (list[Any]): backupLocations defines the list of desired configuration to use for
              BackupStorageLocations

            configuration (dict[str, Any]): configuration is used to configure the data protection application's
              server config

            features (dict[str, Any]): features defines the configuration for the DPA to enable the OADP tech
              preview features

            image_pull_policy (str): which imagePullPolicy to use in all container images used by OADP. By
              default, for images with sha256 or sha512 digest, OADP uses
              IfNotPresent and uses Always for all other images.

            pod_annotations (dict[str, Any]): add annotations to pods deployed by operator

            pod_dns_config (dict[str, Any]): podDnsConfig defines the DNS parameters of a pod in addition to those
              generated from DNSPolicy.
              https://kubernetes.io/docs/concepts/services-networking/dns-pod-
              service/#pod-dns-config

            pod_dns_policy (str): podDnsPolicy defines how a pod's DNS will be configured.
              https://kubernetes.io/docs/concepts/services-networking/dns-pod-
              service/#pod-s-dns-policy

            snapshot_locations (list[Any]): snapshotLocations defines the list of desired configuration to use for
              VolumeSnapshotLocations

            unsupported_overrides (dict[str, Any]): unsupportedOverrides can be used to override images used in
              deployments. Available keys are:   - veleroImageFqin   -
              awsPluginImageFqin   - legacyAWSPluginImageFqin   -
              openshiftPluginImageFqin   - azurePluginImageFqin   -
              gcpPluginImageFqin   - resticRestoreImageFqin   -
              kubevirtPluginImageFqin   - operator-type

        """
        super().__init__(**kwargs)

        self.backup_images = backup_images
        self.backup_locations = backup_locations
        self.configuration = configuration
        self.features = features
        self.image_pull_policy = image_pull_policy
        self.pod_annotations = pod_annotations
        self.pod_dns_config = pod_dns_config
        self.pod_dns_policy = pod_dns_policy
        self.snapshot_locations = snapshot_locations
        self.unsupported_overrides = unsupported_overrides

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.configuration is None:
                raise MissingRequiredArgumentError(argument="self.configuration")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["configuration"] = self.configuration

            if self.backup_images is not None:
                _spec["backupImages"] = self.backup_images

            if self.backup_locations is not None:
                _spec["backupLocations"] = self.backup_locations

            if self.features is not None:
                _spec["features"] = self.features

            if self.image_pull_policy is not None:
                _spec["imagePullPolicy"] = self.image_pull_policy

            if self.pod_annotations is not None:
                _spec["podAnnotations"] = self.pod_annotations

            if self.pod_dns_config is not None:
                _spec["podDnsConfig"] = self.pod_dns_config

            if self.pod_dns_policy is not None:
                _spec["podDnsPolicy"] = self.pod_dns_policy

            if self.snapshot_locations is not None:
                _spec["snapshotLocations"] = self.snapshot_locations

            if self.unsupported_overrides is not None:
                _spec["unsupportedOverrides"] = self.unsupported_overrides

    # End of generated code
