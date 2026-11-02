# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md


from typing import Any

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.resource import NamespacedResource


class BareMetalHost(NamespacedResource):
    """
    BareMetalHost is the Schema for the baremetalhosts API
    """

    api_group: str = NamespacedResource.ApiGroup.METAL3_IO

    def __init__(
        self,
        architecture: str | None = None,
        automated_cleaning_mode: str | None = None,
        bmc: dict[str, Any] | None = None,
        boot_mac_address: str | None = None,
        boot_mode: str | None = None,
        consumer_ref: dict[str, Any] | None = None,
        custom_deploy: dict[str, Any] | None = None,
        description: str | None = None,
        disable_power_off: bool | None = None,
        externally_provisioned: bool | None = None,
        firmware: dict[str, Any] | None = None,
        hardware_profile: str | None = None,
        image: dict[str, Any] | None = None,
        inspection_mode: str | None = None,
        meta_data: dict[str, Any] | None = None,
        network_data: dict[str, Any] | None = None,
        network_interfaces: list[Any] | None = None,
        online: bool | None = None,
        preprovisioning_network_data_name: str | None = None,
        raid: dict[str, Any] | None = None,
        root_device_hints: dict[str, Any] | None = None,
        taints: list[Any] | None = None,
        user_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            architecture (str): CPU architecture of the host, e.g. "x86_64" or "aarch64". If unset,
              eventually populated by inspection.

            automated_cleaning_mode (str): When set to disabled, automated cleaning will be skipped during
              provisioning and deprovisioning.

            bmc (dict[str, Any]): How do we connect to the BMC (Baseboard Management Controller) on the
              host?

            boot_mac_address (str): The MAC address of the NIC used for provisioning the host. In case of
              network boot, this is the MAC address of the PXE booting
              interface. The MAC address of the BMC must never be used here!

            boot_mode (str): Select the method of initializing the hardware during boot. Defaults
              to UEFI. Legacy boot should only be used for hardware that does
              not support UEFI correctly. Set to UEFISecureBoot to turn secure
              boot on automatically after provisioning.

            consumer_ref (dict[str, Any]): ConsumerRef can be used to store information about something that is
              using a host. When it is not empty, the host is considered "in
              use". The common use case is a link to a Machine resource when the
              host is used by Cluster API.

            custom_deploy (dict[str, Any]): A custom deploy procedure. This is an advanced feature that allows
              using a custom deploy step provided by a site-specific deployment
              ramdisk. Most users will want to use "image" instead. Setting this
              field triggers provisioning.

            description (str): Description is a human-entered text used to help identify the host.

            disable_power_off (bool): When set to true, power off of the node will be disabled, instead, a
              reboot will be used in place of power on/off

            externally_provisioned (bool): ExternallyProvisioned means something else has provisioned the image
              running on the host, and the operator should only manage the power
              status. This field is used for integration with already
              provisioned hosts and when pivoting hosts between clusters.  This
              field can be set to true either: 1. During initial host creation
              (e.g., for pre-provisioned hosts) 2. After inspection completes
              when the host reaches Available state  When used in environments
              with Cluster API Provider Metal3 (CAPM3), ensure hosts are labeled
              appropriately so CAPM3's host selector can distinguish them from
              CAPM3-managed hosts. If unsure, leave this field as false.

            firmware (dict[str, Any]): Firmware (BIOS) configuration for bare metal server. If set, the
              requested settings will be applied before the host is provisioned.
              Deprecated: no longer supported by any driver. An alternative is
              to use HostFirmwareSettings resources that allow changing
              arbitrary values and support the generic Redfish-based drivers.

            hardware_profile (str): What is the name of the hardware profile for this host? Hardware
              profiles are deprecated and should not be used. Use the separate
              fields Architecture and RootDeviceHints instead. Set to "empty" to
              prepare for the future version of the API without hardware
              profiles.

            image (dict[str, Any]): Image holds the details of the image to be provisioned. Populating the
              image will cause the host to start provisioning.

            inspection_mode (str): Specifies the mode for host inspection. "disabled" - no inspection
              will be performed "agent" - normal agent-based inspection will run

            meta_data (dict[str, Any]): MetaData holds the reference to the Secret containing host metadata
              which is passed to the Config Drive. By default, metadata will be
              generated for the host, so most users do not need to set this
              field.

            network_data (dict[str, Any]): NetworkData holds the reference to the Secret containing network
              configuration which is passed to the Config Drive and interpreted
              by the first boot software such as cloud-init.

            network_interfaces (list[Any]): NetworkInterfaces defines the network configuration for each
              interface. This will be used to configure switch ports for the
              host.  Interface names must correspond to actual NICs discovered
              during inspection (see HardwareData resource).  They are
              referenced by either the name or MAC address of the NIC.

            online (bool): Should the host be powered on? If the host is currently in a stable
              state (e.g. provisioned), its power state will be forced to match
              this value.

            preprovisioning_network_data_name (str): PreprovisioningNetworkDataName is the name of the Secret in the local
              namespace containing network configuration which is passed to the
              preprovisioning image, and to the Config Drive if not overridden
              by specifying NetworkData.

            raid (dict[str, Any]): RAID configuration for bare metal server. If set, the RAID settings
              will be applied before the host is provisioned. If not, the
              current settings will not be modified. Only one of the sub-fields
              hardwareRAIDVolumes and softwareRAIDVolumes can be set at the same
              time.

            root_device_hints (dict[str, Any]): Provide guidance about how to choose the device for the image being
              provisioned. The default is currently to use /dev/sda as the root
              device.

            taints (list[Any]): Taints is the full, authoritative list of taints to apply to the
              corresponding Machine. This list will overwrite any modifications
              made to the Machine on an ongoing basis.

            user_data (dict[str, Any]): UserData holds the reference to the Secret containing the user data
              which is passed to the Config Drive and interpreted by the first-
              boot software such as cloud-init. The format of user data is
              specific to the first-boot software.

        """
        super().__init__(**kwargs)

        self.architecture = architecture
        self.automated_cleaning_mode = automated_cleaning_mode
        self.bmc = bmc
        self.boot_mac_address = boot_mac_address
        self.boot_mode = boot_mode
        self.consumer_ref = consumer_ref
        self.custom_deploy = custom_deploy
        self.description = description
        self.disable_power_off = disable_power_off
        self.externally_provisioned = externally_provisioned
        self.firmware = firmware
        self.hardware_profile = hardware_profile
        self.image = image
        self.inspection_mode = inspection_mode
        self.meta_data = meta_data
        self.network_data = network_data
        self.network_interfaces = network_interfaces
        self.online = online
        self.preprovisioning_network_data_name = preprovisioning_network_data_name
        self.raid = raid
        self.root_device_hints = root_device_hints
        self.taints = taints
        self.user_data = user_data

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.online is None:
                raise MissingRequiredArgumentError(argument="self.online")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["online"] = self.online

            if self.architecture is not None:
                _spec["architecture"] = self.architecture

            if self.automated_cleaning_mode is not None:
                _spec["automatedCleaningMode"] = self.automated_cleaning_mode

            if self.bmc is not None:
                _spec["bmc"] = self.bmc

            if self.boot_mac_address is not None:
                _spec["bootMACAddress"] = self.boot_mac_address

            if self.boot_mode is not None:
                _spec["bootMode"] = self.boot_mode

            if self.consumer_ref is not None:
                _spec["consumerRef"] = self.consumer_ref

            if self.custom_deploy is not None:
                _spec["customDeploy"] = self.custom_deploy

            if self.description is not None:
                _spec["description"] = self.description

            if self.disable_power_off is not None:
                _spec["disablePowerOff"] = self.disable_power_off

            if self.externally_provisioned is not None:
                _spec["externallyProvisioned"] = self.externally_provisioned

            if self.firmware is not None:
                _spec["firmware"] = self.firmware

            if self.hardware_profile is not None:
                _spec["hardwareProfile"] = self.hardware_profile

            if self.image is not None:
                _spec["image"] = self.image

            if self.inspection_mode is not None:
                _spec["inspectionMode"] = self.inspection_mode

            if self.meta_data is not None:
                _spec["metaData"] = self.meta_data

            if self.network_data is not None:
                _spec["networkData"] = self.network_data

            if self.network_interfaces is not None:
                _spec["networkInterfaces"] = self.network_interfaces

            if self.preprovisioning_network_data_name is not None:
                _spec["preprovisioningNetworkDataName"] = self.preprovisioning_network_data_name

            if self.raid is not None:
                _spec["raid"] = self.raid

            if self.root_device_hints is not None:
                _spec["rootDeviceHints"] = self.root_device_hints

            if self.taints is not None:
                _spec["taints"] = self.taints

            if self.user_data is not None:
                _spec["userData"] = self.user_data

    # End of generated code
