# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.resource import NamespacedResource


class Conversion(NamespacedResource):
    """
    Conversion is the Schema for the conversions API
    """

    api_group: str = NamespacedResource.ApiGroup.FORKLIFT_KONVEYOR_IO

    def __init__(
        self,
        connection: dict[str, Any] | None = None,
        destination: dict[str, Any] | None = None,
        disk_encryption: dict[str, Any] | None = None,
        disks: list[Any] | None = None,
        extra_mounts: list[Any] | None = None,
        extra_volumes: list[Any] | None = None,
        image: str | None = None,
        local_migration: bool | None = None,
        pod_settings: dict[str, Any] | None = None,
        settings: dict[str, Any] | None = None,
        target_namespace: str | None = None,
        type: str | None = None,
        vddk_image: str | None = None,
        vm: dict[str, Any] | None = None,
        xfs_compatibility: bool | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            connection (dict[str, Any]): Source connection details including the virt-v2v credentials secret.

            destination (dict[str, Any]): Reference to the destination provider where pods and PVCs live. When
              nil or pointing to the host provider the local client is used;
              otherwise a remote k8s client is constructed from the provider URL
              and its secret.

            disk_encryption (dict[str, Any]): DiskEncryption configures how LUKS-encrypted disks are unlocked. Set
              Type=LUKS and populate Secret for passphrase-based unlocking, or
              set Type=Clevis for automated network-based (tang/TPM2) unlocking.

            disks (list[Any]): Disks to be converted or inspected. For InPlace/Remote: populated from
              PVCs (namespaced name + volume mode). For Inspection: populated
              with disk paths from the source inventory.

            extra_mounts (list[Any]): Extra volume mounts to add to the conversion pod container.

            extra_volumes (list[Any]): Extra volumes to add to the conversion pod (e.g. provider storage
              PVCs).

            image (str): Container image for the virt-v2v pod. When empty the controller falls
              back to the global default from settings.

            local_migration (bool): Sets LOCAL_MIGRATION env var in the conversion pod.

            pod_settings (dict[str, Any]): Pod-level overrides for the conversion pod.

            settings (dict[str, Any]): Freeform settings passed to the conversion process as environment
              variables.

            target_namespace (str): Namespace where conversion pods will be created. Defaults to the
              Conversion CR's own namespace.

            type (str): Type of conversion.

            vddk_image (str): VDDK init container image. Required when type is DeepInspection. For
              other types, empty means no VDDK sidecar.

            vm (dict[str, Any]): Reference to the source VM.

            xfs_compatibility (bool): XfsCompatibility selects the XFS-compatible virt-v2v image variant.

        """
        super().__init__(**kwargs)

        self.connection = connection
        self.destination = destination
        self.disk_encryption = disk_encryption
        self.disks = disks
        self.extra_mounts = extra_mounts
        self.extra_volumes = extra_volumes
        self.image = image
        self.local_migration = local_migration
        self.pod_settings = pod_settings
        self.settings = settings
        self.target_namespace = target_namespace
        self.type = type
        self.vddk_image = vddk_image
        self.vm = vm
        self.xfs_compatibility = xfs_compatibility

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.connection is None:
                raise MissingRequiredArgumentError(argument="self.connection")

            if self.type is None:
                raise MissingRequiredArgumentError(argument="self.type")

            if self.vm is None:
                raise MissingRequiredArgumentError(argument="self.vm")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["connection"] = self.connection
            _spec["type"] = self.type
            _spec["vm"] = self.vm

            if self.destination is not None:
                _spec["destination"] = self.destination

            if self.disk_encryption is not None:
                _spec["diskEncryption"] = self.disk_encryption

            if self.disks is not None:
                _spec["disks"] = self.disks

            if self.extra_mounts is not None:
                _spec["extraMounts"] = self.extra_mounts

            if self.extra_volumes is not None:
                _spec["extraVolumes"] = self.extra_volumes

            if self.image is not None:
                _spec["image"] = self.image

            if self.local_migration is not None:
                _spec["localMigration"] = self.local_migration

            if self.pod_settings is not None:
                _spec["podSettings"] = self.pod_settings

            if self.settings is not None:
                _spec["settings"] = self.settings

            if self.target_namespace is not None:
                _spec["targetNamespace"] = self.target_namespace

            if self.vddk_image is not None:
                _spec["vddkImage"] = self.vddk_image

            if self.xfs_compatibility is not None:
                _spec["xfsCompatibility"] = self.xfs_compatibility

    # End of generated code
