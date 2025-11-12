# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import Resource


class VirtualMachineClusterPreference(Resource):
    """
    VirtualMachineClusterPreference is a cluster scoped version of the VirtualMachinePreference resource.
    """

    api_group: str = Resource.ApiGroup.INSTANCETYPE_KUBEVIRT_IO

    def __init__(
        self,
        spec_annotations: dict[str, Any] | None = None,
        clock: dict[str, Any] | None = None,
        cpu: dict[str, Any] | None = None,
        devices: dict[str, Any] | None = None,
        features: dict[str, Any] | None = None,
        firmware: dict[str, Any] | None = None,
        machine: dict[str, Any] | None = None,
        prefer_spread_socket_to_core_ratio: int | None = None,
        preferred_subdomain: str | None = None,
        preferred_termination_grace_period_seconds: int | None = None,
        requirements: dict[str, Any] | None = None,
        volumes: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            spec_annotations (dict[str, Any]): Optionally defines preferred Annotations to be applied to the
              VirtualMachineInstance

            clock (dict[str, Any]): Clock optionally defines preferences associated with the Clock
              attribute of a VirtualMachineInstance DomainSpec

            cpu (dict[str, Any]): CPU optionally defines preferences associated with the CPU attribute
              of a VirtualMachineInstance DomainSpec

            devices (dict[str, Any]): Devices optionally defines preferences associated with the Devices
              attribute of a VirtualMachineInstance DomainSpec

            features (dict[str, Any]): Features optionally defines preferences associated with the Features
              attribute of a VirtualMachineInstance DomainSpec

            firmware (dict[str, Any]): Firmware optionally defines preferences associated with the Firmware
              attribute of a VirtualMachineInstance DomainSpec

            machine (dict[str, Any]): Machine optionally defines preferences associated with the Machine
              attribute of a VirtualMachineInstance DomainSpec

            prefer_spread_socket_to_core_ratio (int): PreferSpreadSocketToCoreRatio defines the ratio to spread vCPUs
              between cores and sockets, it defaults to 2.

            preferred_subdomain (str): Subdomain of the VirtualMachineInstance

            preferred_termination_grace_period_seconds (int): Grace period observed after signalling a VirtualMachineInstance to
              stop after which the VirtualMachineInstance is force terminated.

            requirements (dict[str, Any]): Requirements defines the minium amount of instance type defined
              resources required by a set of preferences

            volumes (dict[str, Any]): Volumes optionally defines preferences associated with the Volumes
              attribute of a VirtualMachineInstace DomainSpec

        """
        super().__init__(**kwargs)

        self.spec_annotations = spec_annotations
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

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.spec_annotations is not None:
                _spec["annotations"] = self.spec_annotations

            if self.clock is not None:
                _spec["clock"] = self.clock

            if self.cpu is not None:
                _spec["cpu"] = self.cpu

            if self.devices is not None:
                _spec["devices"] = self.devices

            if self.features is not None:
                _spec["features"] = self.features

            if self.firmware is not None:
                _spec["firmware"] = self.firmware

            if self.machine is not None:
                _spec["machine"] = self.machine

            if self.prefer_spread_socket_to_core_ratio is not None:
                _spec["preferSpreadSocketToCoreRatio"] = self.prefer_spread_socket_to_core_ratio

            if self.preferred_subdomain is not None:
                _spec["preferredSubdomain"] = self.preferred_subdomain

            if self.preferred_termination_grace_period_seconds is not None:
                _spec["preferredTerminationGracePeriodSeconds"] = self.preferred_termination_grace_period_seconds

            if self.requirements is not None:
                _spec["requirements"] = self.requirements

            if self.volumes is not None:
                _spec["volumes"] = self.volumes

    # End of generated code
