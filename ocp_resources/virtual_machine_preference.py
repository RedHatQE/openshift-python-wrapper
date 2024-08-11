# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, Optional
from ocp_resources.resource import NamespacedResource


class VirtualMachinePreference(NamespacedResource):
    """
    VirtualMachinePreference resource contains optional preferences related to
    the VirtualMachine.
    """

    api_group: str = NamespacedResource.ApiGroup.INSTANCETYPE_KUBEVIRT_IO

    def __init__(
        self,
        annotations: Optional[Dict[str, Any]] = None,
        clock: Optional[Dict[str, Any]] = None,
        cpu: Optional[Dict[str, Any]] = None,
        devices: Optional[Dict[str, Any]] = None,
        features: Optional[Dict[str, Any]] = None,
        firmware: Optional[Dict[str, Any]] = None,
        machine: Optional[Dict[str, Any]] = None,
        prefer_spread_socket_to_core_ratio: Optional[int] = None,
        preferred_subdomain: Optional[str] = "",
        preferred_termination_grace_period_seconds: Optional[int] = None,
        requirements: Optional[Dict[str, Any]] = None,
        volumes: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            annotations(Dict[Any, Any]): Optionally defines preferred Annotations to be applied to the
              VirtualMachineInstance

            clock(Dict[Any, Any]): Clock optionally defines preferences associated with the Clock attribute of
              a VirtualMachineInstance DomainSpec

              FIELDS:
                preferredClockOffset	<Object>
                  ClockOffset allows specifying the UTC offset or the timezone of the guest
                  clock.

                preferredTimer	<Object>
                  Timer specifies whih timers are attached to the vmi.

            cpu(Dict[Any, Any]): CPU optionally defines preferences associated with the CPU attribute of a
              VirtualMachineInstance DomainSpec

              FIELDS:
                preferredCPUFeatures	<[]Object>
                  PreferredCPUFeatures optionally defines a slice of preferred CPU features.

                preferredCPUTopology	<string>
                  PreferredCPUTopology optionally defines the preferred guest visible CPU
                  topology, defaults to PreferSockets.

            devices(Dict[Any, Any]): Devices optionally defines preferences associated with the Devices attribute
              of a VirtualMachineInstance DomainSpec

              FIELDS:
                preferredAutoattachGraphicsDevice	<boolean>
                  PreferredAutoattachGraphicsDevice optionally defines the preferred value of
                  AutoattachGraphicsDevice

                preferredAutoattachInputDevice	<boolean>
                  PreferredAutoattachInputDevice optionally defines the preferred value of
                  AutoattachInputDevice

                preferredAutoattachMemBalloon	<boolean>
                  PreferredAutoattachMemBalloon optionally defines the preferred value of
                  AutoattachMemBalloon

                preferredAutoattachPodInterface	<boolean>
                  PreferredAutoattachPodInterface optionally defines the preferred value of
                  AutoattachPodInterface

                preferredAutoattachSerialConsole	<boolean>
                  PreferredAutoattachSerialConsole optionally defines the preferred value of
                  AutoattachSerialConsole

                preferredBlockMultiQueue	<boolean>
                  PreferredBlockMultiQueue optionally enables the vhost multiqueue feature for
                  virtio disks.

                preferredCdromBus	<string>
                  PreferredCdromBus optionally defines the preferred bus for Cdrom Disk
                  devices.

                preferredDisableHotplug	<boolean>
                  PreferredDisableHotplug optionally defines the preferred value of
                  DisableHotplug

                preferredDiskBlockSize	<Object>
                  PreferredBlockSize optionally defines the block size of Disk devices.

                preferredDiskBus	<string>
                  PreferredDiskBus optionally defines the preferred bus for Disk Disk devices.

                preferredDiskCache	<string>
                  PreferredCache optionally defines the DriverCache to be used by Disk
                  devices.

                preferredDiskDedicatedIoThread	<boolean>
                  PreferredDedicatedIoThread optionally enables dedicated IO threads for Disk
                  devices using the virtio bus.

                preferredDiskIO	<string>
                  PreferredIo optionally defines the QEMU disk IO mode to be used by Disk
                  devices.

                preferredInputBus	<string>
                  PreferredInputBus optionally defines the preferred bus for Input devices.

                preferredInputType	<string>
                  PreferredInputType optionally defines the preferred type for Input devices.

                preferredInterfaceMasquerade	<Object>
                  PreferredInterfaceMasquerade optionally defines the preferred masquerade
                  configuration to use with each network interface.

                preferredInterfaceModel	<string>
                  PreferredInterfaceModel optionally defines the preferred model to be used by
                  Interface devices.

                preferredLunBus	<string>
                  PreferredLunBus optionally defines the preferred bus for Lun Disk devices.

                preferredNetworkInterfaceMultiQueue	<boolean>
                  PreferredNetworkInterfaceMultiQueue optionally enables the vhost multiqueue
                  feature for virtio interfaces.

                preferredRng	<Object>
                  PreferredRng optionally defines the preferred rng device to be used.

                preferredSoundModel	<string>
                  PreferredSoundModel optionally defines the preferred model for Sound
                  devices.

                preferredTPM	<Object>
                  PreferredTPM optionally defines the preferred TPM device to be used.

                preferredUseVirtioTransitional	<boolean>
                  PreferredUseVirtioTransitional optionally defines the preferred value of
                  UseVirtioTransitional

                preferredVirtualGPUOptions	<Object>
                  PreferredVirtualGPUOptions optionally defines the preferred value of
                  VirtualGPUOptions

            features(Dict[Any, Any]): Features optionally defines preferences associated with the Features
              attribute of a VirtualMachineInstance DomainSpec

              FIELDS:
                preferredAcpi	<Object>
                  PreferredAcpi optionally enables the ACPI feature

                preferredApic	<Object>
                  PreferredApic optionally enables and configures the APIC feature

                preferredHyperv	<Object>
                  PreferredHyperv optionally enables and configures HyperV features

                preferredKvm	<Object>
                  PreferredKvm optionally enables and configures KVM features

                preferredPvspinlock	<Object>
                  PreferredPvspinlock optionally enables the Pvspinlock feature

                preferredSmm	<Object>
                  PreferredSmm optionally enables the SMM feature

            firmware(Dict[Any, Any]): Firmware optionally defines preferences associated with the Firmware
              attribute of a VirtualMachineInstance DomainSpec

              FIELDS:
                preferredUseBios	<boolean>
                  PreferredUseBios optionally enables BIOS

                preferredUseBiosSerial	<boolean>
                  PreferredUseBiosSerial optionally transmitts BIOS output over the serial.
                   Requires PreferredUseBios to be enabled.

                preferredUseEfi	<boolean>
                  PreferredUseEfi optionally enables EFI

                preferredUseSecureBoot	<boolean>
                  PreferredUseSecureBoot optionally enables SecureBoot and the OVMF roms will
                  be swapped for SecureBoot-enabled ones.
                   Requires PreferredUseEfi and PreferredSmm to be enabled.

            machine(Dict[Any, Any]): Machine optionally defines preferences associated with the Machine attribute
              of a VirtualMachineInstance DomainSpec

              FIELDS:
                preferredMachineType	<string>
                  PreferredMachineType optionally defines the preferred machine type to use.

            prefer_spread_socket_to_core_ratio(int): PreferSpreadSocketToCoreRatio defines the ratio to spread vCPUs between
              cores and sockets, it defaults to 2.

            preferred_subdomain(str): Subdomain of the VirtualMachineInstance

            preferred_termination_grace_period_seconds(int): Grace period observed after signalling a VirtualMachineInstance to stop
              after which the VirtualMachineInstance is force terminated.

            requirements(Dict[Any, Any]): Requirements defines the minium amount of instance type defined resources
              required by a set of preferences

              FIELDS:
                cpu	<Object>
                  Required CPU related attributes of the instancetype.

                memory	<Object>
                  Required Memory related attributes of the instancetype.

            volumes(Dict[Any, Any]): Volumes optionally defines preferences associated with the Volumes attribute
              of a VirtualMachineInstace DomainSpec

              FIELDS:
                preferredStorageClassName	<string>
                  PreffereedStorageClassName optionally defines the preferred storageClass

        """
        super().__init__(**kwargs)

        self.annotations = annotations
        self.clock = clock
        self.cpu = cpu
        self.devices = devices
        self.features = features
        self.firmware = firmware
        self.machine = machine
        self.prefer_spread_socket_to_core_ratio = prefer_spread_socket_to_core_ratio
        self.preferred_subdomain = preferred_subdomain
        self.preferred_termination_grace_period_seconds = preferred_termination_grace_period_seconds
        self.requirements = requirements
        self.volumes = volumes

    def to_dict(self) -> None:
        super().to_dict()

        if not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.annotations:
                _spec["annotations"] = self.annotations

            if self.clock:
                _spec["clock"] = self.clock

            if self.cpu:
                _spec["cpu"] = self.cpu

            if self.devices:
                _spec["devices"] = self.devices

            if self.features:
                _spec["features"] = self.features

            if self.firmware:
                _spec["firmware"] = self.firmware

            if self.machine:
                _spec["machine"] = self.machine

            if self.prefer_spread_socket_to_core_ratio:
                _spec["preferSpreadSocketToCoreRatio"] = self.prefer_spread_socket_to_core_ratio

            if self.preferred_subdomain:
                _spec["preferredSubdomain"] = self.preferred_subdomain

            if self.preferred_termination_grace_period_seconds:
                _spec["preferredTerminationGracePeriodSeconds"] = self.preferred_termination_grace_period_seconds

            if self.requirements:
                _spec["requirements"] = self.requirements

            if self.volumes:
                _spec["volumes"] = self.volumes
