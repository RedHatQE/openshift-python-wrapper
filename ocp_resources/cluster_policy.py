# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md


from typing import Any

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.resource import Resource


class ClusterPolicy(Resource):
    """
    ClusterPolicy is the Schema for the clusterpolicies API
    """

    api_group: str = Resource.ApiGroup.NVIDIA_COM

    def __init__(
        self,
        cc_manager: dict[str, Any] | None = None,
        cdi: dict[str, Any] | None = None,
        daemonsets: dict[str, Any] | None = None,
        dcgm: dict[str, Any] | None = None,
        dcgm_exporter: dict[str, Any] | None = None,
        device_plugin: dict[str, Any] | None = None,
        driver: dict[str, Any] | None = None,
        gdrcopy: dict[str, Any] | None = None,
        gds: dict[str, Any] | None = None,
        gfd: dict[str, Any] | None = None,
        host_paths: dict[str, Any] | None = None,
        kata_manager: dict[str, Any] | None = None,
        mig: dict[str, Any] | None = None,
        mig_manager: dict[str, Any] | None = None,
        node_status_exporter: dict[str, Any] | None = None,
        operator: dict[str, Any] | None = None,
        psa: dict[str, Any] | None = None,
        psp: dict[str, Any] | None = None,
        sandbox_device_plugin: dict[str, Any] | None = None,
        sandbox_workloads: dict[str, Any] | None = None,
        toolkit: dict[str, Any] | None = None,
        validator: dict[str, Any] | None = None,
        vfio_manager: dict[str, Any] | None = None,
        vgpu_device_manager: dict[str, Any] | None = None,
        vgpu_manager: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            cc_manager (dict[str, Any]): CCManager component spec

            cdi (dict[str, Any]): CDI configures how the Container Device Interface is used in the
              cluster

            daemonsets (dict[str, Any]): Daemonset defines common configuration for all Daemonsets

            dcgm (dict[str, Any]): DCGM component spec

            dcgm_exporter (dict[str, Any]): DCGMExporter spec

            device_plugin (dict[str, Any]): DevicePlugin component spec

            driver (dict[str, Any]): Driver component spec

            gdrcopy (dict[str, Any]): GDRCopy component spec

            gds (dict[str, Any]): GPUDirectStorage defines the spec for GDS components(Experimental)

            gfd (dict[str, Any]): GPUFeatureDiscovery spec

            host_paths (dict[str, Any]): HostPaths defines various paths on the host needed by GPU Operator
              components

            kata_manager (dict[str, Any]): KataManager component spec

            mig (dict[str, Any]): MIG spec

            mig_manager (dict[str, Any]): MIGManager for configuration to deploy MIG Manager

            node_status_exporter (dict[str, Any]): NodeStatusExporter spec

            operator (dict[str, Any]): Operator component spec

            psa (dict[str, Any]): PSA defines spec for PodSecurityAdmission configuration

            psp (dict[str, Any]): Deprecated: Pod Security Policies are no longer supported. Please use
              PodSecurityAdmission instead PSP defines spec for handling
              PodSecurityPolicies

            sandbox_device_plugin (dict[str, Any]): SandboxDevicePlugin component spec

            sandbox_workloads (dict[str, Any]): SandboxWorkloads defines the spec for handling sandbox workloads (i.e.
              Virtual Machines)

            toolkit (dict[str, Any]): Toolkit component spec

            validator (dict[str, Any]): Validator defines the spec for operator-validator daemonset

            vfio_manager (dict[str, Any]): VFIOManager for configuration to deploy VFIO-PCI Manager

            vgpu_device_manager (dict[str, Any]): VGPUDeviceManager spec

            vgpu_manager (dict[str, Any]): VGPUManager component spec

        """
        super().__init__(**kwargs)

        self.cc_manager = cc_manager
        self.cdi = cdi
        self.daemonsets = daemonsets
        self.dcgm = dcgm
        self.dcgm_exporter = dcgm_exporter
        self.device_plugin = device_plugin
        self.driver = driver
        self.gdrcopy = gdrcopy
        self.gds = gds
        self.gfd = gfd
        self.host_paths = host_paths
        self.kata_manager = kata_manager
        self.mig = mig
        self.mig_manager = mig_manager
        self.node_status_exporter = node_status_exporter
        self.operator = operator
        self.psa = psa
        self.psp = psp
        self.sandbox_device_plugin = sandbox_device_plugin
        self.sandbox_workloads = sandbox_workloads
        self.toolkit = toolkit
        self.validator = validator
        self.vfio_manager = vfio_manager
        self.vgpu_device_manager = vgpu_device_manager
        self.vgpu_manager = vgpu_manager

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.daemonsets is None:
                raise MissingRequiredArgumentError(argument="self.daemonsets")

            if self.dcgm is None:
                raise MissingRequiredArgumentError(argument="self.dcgm")

            if self.dcgm_exporter is None:
                raise MissingRequiredArgumentError(argument="self.dcgm_exporter")

            if self.device_plugin is None:
                raise MissingRequiredArgumentError(argument="self.device_plugin")

            if self.driver is None:
                raise MissingRequiredArgumentError(argument="self.driver")

            if self.gfd is None:
                raise MissingRequiredArgumentError(argument="self.gfd")

            if self.node_status_exporter is None:
                raise MissingRequiredArgumentError(argument="self.node_status_exporter")

            if self.operator is None:
                raise MissingRequiredArgumentError(argument="self.operator")

            if self.toolkit is None:
                raise MissingRequiredArgumentError(argument="self.toolkit")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["daemonsets"] = self.daemonsets
            _spec["dcgm"] = self.dcgm
            _spec["dcgmExporter"] = self.dcgm_exporter
            _spec["devicePlugin"] = self.device_plugin
            _spec["driver"] = self.driver
            _spec["gfd"] = self.gfd
            _spec["nodeStatusExporter"] = self.node_status_exporter
            _spec["operator"] = self.operator
            _spec["toolkit"] = self.toolkit

            if self.cc_manager is not None:
                _spec["ccManager"] = self.cc_manager

            if self.cdi is not None:
                _spec["cdi"] = self.cdi

            if self.gdrcopy is not None:
                _spec["gdrcopy"] = self.gdrcopy

            if self.gds is not None:
                _spec["gds"] = self.gds

            if self.host_paths is not None:
                _spec["hostPaths"] = self.host_paths

            if self.kata_manager is not None:
                _spec["kataManager"] = self.kata_manager

            if self.mig is not None:
                _spec["mig"] = self.mig

            if self.mig_manager is not None:
                _spec["migManager"] = self.mig_manager

            if self.psa is not None:
                _spec["psa"] = self.psa

            if self.psp is not None:
                _spec["psp"] = self.psp

            if self.sandbox_device_plugin is not None:
                _spec["sandboxDevicePlugin"] = self.sandbox_device_plugin

            if self.sandbox_workloads is not None:
                _spec["sandboxWorkloads"] = self.sandbox_workloads

            if self.validator is not None:
                _spec["validator"] = self.validator

            if self.vfio_manager is not None:
                _spec["vfioManager"] = self.vfio_manager

            if self.vgpu_device_manager is not None:
                _spec["vgpuDeviceManager"] = self.vgpu_device_manager

            if self.vgpu_manager is not None:
                _spec["vgpuManager"] = self.vgpu_manager

    # End of generated code
