# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md


from typing import Any

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.resource import NamespacedResource


class CopyAppliance(NamespacedResource):
    """
        CopyAppliance is the Schema for API which causes copy appliances to be created
    in source hypervisors to facilitate disk transfer.
    """

    api_group: str = NamespacedResource.ApiGroup.FORKLIFT_KONVEYOR_IO

    def __init__(
        self,
        attach_disks: list[Any] | None = None,
        container_image: str | None = None,
        datacenter: str | None = None,
        datastore: str | None = None,
        folder: str | None = None,
        provider: dict[str, Any] | None = None,
        resource_pool: str | None = None,
        secret: dict[str, Any] | None = None,
        template: str | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            attach_disks (list[Any]): Disks to attach to the appliance VM for export. Each entry names an
              existing VMDK and carries the VMware identifiers needed to
              correlate guest exports with source inventory. Empty means disks
              should be detached (release); non-empty means they should be
              attached and exporting. Changing the set while terminal re-enters
              the export itinerary. Capped so that the root disk plus the
              attached disks fit within the four SCSI controllers vSphere
              permits per VM (4 x 15 addressable units = 60 disks).

            container_image (str): Fully qualified pull spec for the container image loaded into the
              appliance's podman store. A setup pod reads the image and streams
              it to the appliance over SSH, so the appliance needs no registry
              access of its own. The pod carries no credential, so the image has
              to be readable without one.

            datacenter (str): Datacenter in which the appliance VM is created.

            datastore (str): Datastore that holds the appliance VM home directory.

            folder (str): Inventory folder in which the appliance VM is created.

            provider (dict[str, Any]): Source provider in which the appliance VM is created.

            resource_pool (str): Resource pool in which the appliance VM is created.

            secret (dict[str, Any]): Secret holding everything the controller reaches the appliance with.
              Name is required; Namespace defaults to the CopyAppliance
              namespace.  The SSH private key is read from the "private-key"
              data key; the matching public key is expected to be installed in
              the appliance image already.  The mutual-TLS material the
              appliance serves its exports with is read from the data keys named
              for the files the appliance expects (see pkg/nbd-
              container/announce). The controller installs the CA and the server
              half on the appliance and keeps the client half to query the
              exports with.  Server cert is minted at setup with DNS SAN "nbd-
              server" and an IP SAN for the guest address (nbds://). CA key
              stays in this secret for that mint.

            template (str): Inventory path of the VM template the appliance is cloned from. The
              template supplies the root disk, so it must support the controller
              its disks are attached to, and the one network the appliance is
              reached on, which the clone inherits as-is.

        """
        super().__init__(**kwargs)

        self.attach_disks = attach_disks
        self.container_image = container_image
        self.datacenter = datacenter
        self.datastore = datastore
        self.folder = folder
        self.provider = provider
        self.resource_pool = resource_pool
        self.secret = secret
        self.template = template

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.container_image is None:
                raise MissingRequiredArgumentError(argument="self.container_image")

            if self.datastore is None:
                raise MissingRequiredArgumentError(argument="self.datastore")

            if self.folder is None:
                raise MissingRequiredArgumentError(argument="self.folder")

            if self.provider is None:
                raise MissingRequiredArgumentError(argument="self.provider")

            if self.resource_pool is None:
                raise MissingRequiredArgumentError(argument="self.resource_pool")

            if self.secret is None:
                raise MissingRequiredArgumentError(argument="self.secret")

            if self.template is None:
                raise MissingRequiredArgumentError(argument="self.template")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["containerImage"] = self.container_image
            _spec["datastore"] = self.datastore
            _spec["folder"] = self.folder
            _spec["provider"] = self.provider
            _spec["resourcePool"] = self.resource_pool
            _spec["secret"] = self.secret
            _spec["template"] = self.template

            if self.attach_disks is not None:
                _spec["attachDisks"] = self.attach_disks

            if self.datacenter is not None:
                _spec["datacenter"] = self.datacenter

    # End of generated code
