# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any
from ocp_resources.resource import NamespacedResource


class KubeVirt(NamespacedResource):
    """
    KubeVirt represents the object deploying all KubeVirt resources
    """

    api_group: str = NamespacedResource.ApiGroup.KUBEVIRT_IO

    def __init__(
        self,
        certificate_rotate_strategy: dict[str, Any] | None = None,
        configuration: dict[str, Any] | None = None,
        customize_components: dict[str, Any] | None = None,
        image_pull_policy: str | None = None,
        image_pull_secrets: list[Any] | None = None,
        image_registry: str | None = None,
        image_tag: str | None = None,
        infra: dict[str, Any] | None = None,
        monitor_account: str | None = None,
        monitor_namespace: str | None = None,
        product_component: str | None = None,
        product_name: str | None = None,
        product_version: str | None = None,
        service_monitor_namespace: str | None = None,
        uninstall_strategy: str | None = None,
        workload_update_strategy: dict[str, Any] | None = None,
        workloads: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            certificate_rotate_strategy (dict[str, Any]): No field description from API

            configuration (dict[str, Any]): holds kubevirt configurations. same as the virt-configMap

            customize_components (dict[str, Any]): No field description from API

            image_pull_policy (str): The ImagePullPolicy to use.

            image_pull_secrets (list[Any]): The imagePullSecrets to pull the container images from Defaults to
              none

            image_registry (str): The image registry to pull the container images from Defaults to the
              same registry the operator's container image is pulled from.

            image_tag (str): The image tag to use for the continer images installed. Defaults to
              the same tag as the operator's container image.

            infra (dict[str, Any]): selectors and tolerations that should apply to KubeVirt infrastructure
              components

            monitor_account (str): The name of the Prometheus service account that needs read-access to
              KubeVirt endpoints Defaults to prometheus-k8s

            monitor_namespace (str): The namespace Prometheus is deployed in Defaults to openshift-monitor

            product_component (str): Designate the apps.kubevirt.io/component label for KubeVirt
              components. Useful if KubeVirt is included as part of a product.
              If ProductComponent is not specified, the component label default
              value is kubevirt.

            product_name (str): Designate the apps.kubevirt.io/part-of label for KubeVirt components.
              Useful if KubeVirt is included as part of a product. If
              ProductName is not specified, the part-of label will be omitted.

            product_version (str): Designate the apps.kubevirt.io/version label for KubeVirt components.
              Useful if KubeVirt is included as part of a product. If
              ProductVersion is not specified, KubeVirt's version will be used.

            service_monitor_namespace (str): The namespace the service monitor will be deployed  When
              ServiceMonitorNamespace is set, then we'll install the service
              monitor object in that namespace otherwise we will use the
              monitoring namespace.

            uninstall_strategy (str): Specifies if kubevirt can be deleted if workloads are still present.
              This is mainly a precaution to avoid accidental data loss

            workload_update_strategy (dict[str, Any]): WorkloadUpdateStrategy defines at the cluster level how to handle
              automated workload updates

            workloads (dict[str, Any]): selectors and tolerations that should apply to KubeVirt workloads

        """
        super().__init__(**kwargs)

        self.certificate_rotate_strategy = certificate_rotate_strategy
        self.configuration = configuration
        self.customize_components = customize_components
        self.image_pull_policy = image_pull_policy
        self.image_pull_secrets = image_pull_secrets
        self.image_registry = image_registry
        self.image_tag = image_tag
        self.infra = infra
        self.monitor_account = monitor_account
        self.monitor_namespace = monitor_namespace
        self.product_component = product_component
        self.product_name = product_name
        self.product_version = product_version
        self.service_monitor_namespace = service_monitor_namespace
        self.uninstall_strategy = uninstall_strategy
        self.workload_update_strategy = workload_update_strategy
        self.workloads = workloads

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.certificate_rotate_strategy is not None:
                _spec["certificateRotateStrategy"] = self.certificate_rotate_strategy

            if self.configuration is not None:
                _spec["configuration"] = self.configuration

            if self.customize_components is not None:
                _spec["customizeComponents"] = self.customize_components

            if self.image_pull_policy is not None:
                _spec["imagePullPolicy"] = self.image_pull_policy

            if self.image_pull_secrets is not None:
                _spec["imagePullSecrets"] = self.image_pull_secrets

            if self.image_registry is not None:
                _spec["imageRegistry"] = self.image_registry

            if self.image_tag is not None:
                _spec["imageTag"] = self.image_tag

            if self.infra is not None:
                _spec["infra"] = self.infra

            if self.monitor_account is not None:
                _spec["monitorAccount"] = self.monitor_account

            if self.monitor_namespace is not None:
                _spec["monitorNamespace"] = self.monitor_namespace

            if self.product_component is not None:
                _spec["productComponent"] = self.product_component

            if self.product_name is not None:
                _spec["productName"] = self.product_name

            if self.product_version is not None:
                _spec["productVersion"] = self.product_version

            if self.service_monitor_namespace is not None:
                _spec["serviceMonitorNamespace"] = self.service_monitor_namespace

            if self.uninstall_strategy is not None:
                _spec["uninstallStrategy"] = self.uninstall_strategy

            if self.workload_update_strategy is not None:
                _spec["workloadUpdateStrategy"] = self.workload_update_strategy

            if self.workloads is not None:
                _spec["workloads"] = self.workloads

    # End of generated code
