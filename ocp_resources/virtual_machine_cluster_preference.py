# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, Optional
from ocp_resources.resource import Resource


class VirtualMachineClusterPreference(Resource):
    """
    VirtualMachineClusterPreference is a cluster scoped version of the VirtualMachinePreference resource.
    """

    api_group: str = Resource.ApiGroup.INSTANCETYPE_KUBEVIRT_IO

    def __init__(
        self,
        spec_annotations: Optional[Dict[str, Any]] = None,
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
            spec_annotations (Dict[str, Any]): Optionally defines preferred Annotations to be applied to the
              VirtualMachineInstance

            clock (Dict[str, Any]): Clock optionally defines preferences associated with the Clock
              attribute of a VirtualMachineInstance DomainSpec

            cpu (Dict[str, Any]): CPU optionally defines preferences associated with the CPU attribute
              of a VirtualMachineInstance DomainSpec

            devices (Dict[str, Any]): Devices optionally defines preferences associated with the Devices
              attribute of a VirtualMachineInstance DomainSpec

            features (Dict[str, Any]): Features optionally defines preferences associated with the Features
              attribute of a VirtualMachineInstance DomainSpec

            firmware (Dict[str, Any]): Firmware optionally defines preferences associated with the Firmware
              attribute of a VirtualMachineInstance DomainSpec

            machine (Dict[str, Any]): Machine optionally defines preferences associated with the Machine
              attribute of a VirtualMachineInstance DomainSpec

            prefer_spread_socket_to_core_ratio (int): PreferSpreadSocketToCoreRatio defines the ratio to spread vCPUs
              between cores and sockets, it defaults to 2.

            preferred_subdomain (str): Subdomain of the VirtualMachineInstance

            preferred_termination_grace_period_seconds (int): Grace period observed after signalling a VirtualMachineInstance to
              stop after which the VirtualMachineInstance is force terminated.

            requirements (Dict[str, Any]): Requirements defines the minium amount of instance type defined
              resources required by a set of preferences

            volumes (Dict[str, Any]): Volumes optionally defines preferences associated with the Volumes
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

            if self.spec_annotations:
                _spec["annotations"] = self.spec_annotations

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

    # End of generated code
