from typing import Any

from ocp_resources.resource import NamespacedResource
from ocp_resources.utils.constants import TIMEOUT_4MINUTES


class Conversion(NamespacedResource):
    """
    Migration Toolkit For Virtualization (MTV) Conversion Resource.

    Args:
        type (str): Conversion type. Valid values: "DeepInspection", "InPlace", "Remote", "Inspection".
        vm_id (str, optional): Source VM managed object ID (e.g., "vm-140"). Either id or name must be specified.
        vm_name (str, optional): Source VM name. Either id or name must be specified.
        vm_namespace (str, optional): Source VM namespace. Required for OpenShift-as-source conversions.
        vm_type (str, optional): Source VM type qualifier.
        connection_secret_name (str): Name of the Secret containing source provider credentials.
        connection_secret_namespace (str): Namespace of the connection Secret.
        target_namespace (str, optional): Namespace where the conversion pod will be created.
        vddk_image (str, optional): VDDK init container image. Required for DeepInspection type.
        disk_encryption_type (str, optional): Disk encryption type. Valid values: "LUKS", "Clevis".
        disk_encryption_secret_name (str, optional): Name of the disk encryption Secret.
            Required when disk_encryption_type is "LUKS".
        disk_encryption_secret_namespace (str, optional): Namespace of the disk encryption Secret.
        xfs_compatibility (bool, optional): Whether to use an XFS-compatible image for VMs
            with XFS v4 filesystems (e.g., RHEL 7).
        settings (dict, optional): Key-value pairs injected as pod environment variables.
            Use "SNAPSHOT_MOREF" key to supply a pre-existing vSphere snapshot.
        image (str, optional): Override the default container image for the conversion pod.
        disks (list, optional): List of disk references for InPlace/Remote conversions.
            Each dict should contain: name, namespace, volumeMode, mountPath or devicePath.
        local_migration (bool, optional): Whether this is a local migration.
        destination_name (str, optional): Name of the remote destination Provider CR.
        destination_namespace (str, optional): Namespace of the remote destination Provider CR.
        pod_settings (dict, optional): Pod configuration overrides. Supported keys:
            requestKVM (bool), nodeSelector (dict), affinity (dict),
            serviceAccount (str), generateName (str), transferNetworkAnnotations (dict).
        extra_volumes (list, optional): Additional volumes for the conversion pod.
        extra_mounts (list, optional): Additional volume mounts for the conversion pod.
    """

    api_group = NamespacedResource.ApiGroup.FORKLIFT_KONVEYOR_IO

    def __init__(
        self,
        type: str | None = None,
        vm_id: str | None = None,
        vm_name: str | None = None,
        vm_namespace: str | None = None,
        vm_type: str | None = None,
        connection_secret_name: str | None = None,
        connection_secret_namespace: str | None = None,
        target_namespace: str | None = None,
        vddk_image: str | None = None,
        disk_encryption_type: str | None = None,
        disk_encryption_secret_name: str | None = None,
        disk_encryption_secret_namespace: str | None = None,
        xfs_compatibility: bool | None = None,
        settings: dict[str, str] | None = None,
        image: str | None = None,
        disks: list[dict[str, Any]] | None = None,
        local_migration: bool | None = None,
        destination_name: str | None = None,
        destination_namespace: str | None = None,
        pod_settings: dict[str, Any] | None = None,
        extra_volumes: list[dict[str, Any]] | None = None,
        extra_mounts: list[dict[str, Any]] | None = None,
        delete_timeout: int = TIMEOUT_4MINUTES,
        **kwargs: Any,
    ) -> None:
        super().__init__(delete_timeout=delete_timeout, **kwargs)
        self.type = type
        self.vm_id = vm_id
        self.vm_name = vm_name
        self.vm_namespace = vm_namespace
        self.vm_type = vm_type
        self.connection_secret_name = connection_secret_name
        self.connection_secret_namespace = connection_secret_namespace
        self.target_namespace = target_namespace
        self.vddk_image = vddk_image
        self.disk_encryption_type = disk_encryption_type
        self.disk_encryption_secret_name = disk_encryption_secret_name
        self.disk_encryption_secret_namespace = disk_encryption_secret_namespace
        self.xfs_compatibility = xfs_compatibility
        self.settings = settings
        self.image = image
        self.disks = disks
        self.local_migration = local_migration
        self.destination_name = destination_name
        self.destination_namespace = destination_namespace
        self.pod_settings = pod_settings
        self.extra_volumes = extra_volumes
        self.extra_mounts = extra_mounts

    def to_dict(self) -> None:
        super().to_dict()
        if not self.kind_dict and not self.yaml_file:
            vm_ref: dict[str, str] = {}
            if self.vm_id is not None:
                vm_ref["id"] = self.vm_id
            if self.vm_name is not None:
                vm_ref["name"] = self.vm_name
            if self.vm_namespace is not None:
                vm_ref["namespace"] = self.vm_namespace
            if self.vm_type is not None:
                vm_ref["type"] = self.vm_type

            self.res.update({
                "spec": {
                    "type": self.type,
                    "vm": vm_ref,
                    "connection": {
                        "secret": {
                            "name": self.connection_secret_name,
                            "namespace": self.connection_secret_namespace,
                        },
                    },
                }
            })

            spec = self.res["spec"]

            if self.target_namespace is not None:
                spec["targetNamespace"] = self.target_namespace

            if self.vddk_image is not None:
                spec["vddkImage"] = self.vddk_image

            if self.disk_encryption_type is not None:
                disk_encryption: dict[str, Any] = {"type": self.disk_encryption_type}
                if self.disk_encryption_secret_name is not None:
                    disk_encryption["secret"] = {
                        "name": self.disk_encryption_secret_name,
                    }
                    if self.disk_encryption_secret_namespace is not None:
                        disk_encryption["secret"]["namespace"] = self.disk_encryption_secret_namespace
                spec["diskEncryption"] = disk_encryption

            if self.xfs_compatibility is not None:
                spec["xfsCompatibility"] = self.xfs_compatibility

            if self.settings is not None:
                spec["settings"] = self.settings

            if self.image is not None:
                spec["image"] = self.image

            if self.disks is not None:
                spec["disks"] = self.disks

            if self.local_migration is not None:
                spec["localMigration"] = self.local_migration

            if self.destination_name is not None:
                spec["destination"] = {"name": self.destination_name}
                if self.destination_namespace is not None:
                    spec["destination"]["namespace"] = self.destination_namespace

            if self.pod_settings is not None:
                spec["podSettings"] = self.pod_settings

            if self.extra_volumes is not None:
                spec["extraVolumes"] = self.extra_volumes

            if self.extra_mounts is not None:
                spec["extraMounts"] = self.extra_mounts
