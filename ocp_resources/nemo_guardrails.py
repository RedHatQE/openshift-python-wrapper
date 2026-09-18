# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md


from typing import Any

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.resource import NamespacedResource


class NemoGuardrails(NamespacedResource):
    """
    NemoGuardrails is the Schema for the nemoguardrails API
    """

    api_group: str = NamespacedResource.ApiGroup.TRUSTYAI_OPENDATAHUB_IO

    def __init__(
        self,
        ca_bundle_config: dict[str, Any] | None = None,
        env: list[Any] | None = None,
        expose_route: bool | None = None,
        nemo_configs: list[Any] | None = None,
        replicas: int | None = None,
        template: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            ca_bundle_config (dict[str, Any]): CABundleConfig defines the CA bundle configuration for custom
              certificates

            env (list[Any]): Define Env information for the main container

            expose_route (bool): ExposeRoute controls whether an external route to the NeMo Guardrails
              server is created. Defaults to true.

            nemo_configs (list[Any]): NemoConfig should be the names of the configmaps containing NeMO
              server configuration files. All files in NemoConfigs will be
              mounted to /app/config/$Name

            replicas (int): Number of replicas for the NeMo Guardrails deployment

            template (dict[str, Any]): Template describes the pod template used by the deployment

        """
        super().__init__(**kwargs)

        self.ca_bundle_config = ca_bundle_config
        self.env = env
        self.expose_route = expose_route
        self.nemo_configs = nemo_configs
        self.replicas = replicas
        self.template = template

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.nemo_configs is None:
                raise MissingRequiredArgumentError(argument="self.nemo_configs")


            self.res["spec"] = {}
            _spec = self.res["spec"]


            _spec["nemoConfigs"] = self.nemo_configs


            if self.ca_bundle_config is not None:
                _spec["caBundleConfig"] = self.ca_bundle_config

            if self.env is not None:
                _spec["env"] = self.env

            if self.expose_route is not None:
                _spec["exposeRoute"] = self.expose_route

            if self.replicas is not None:
                _spec["replicas"] = self.replicas

            if self.template is not None:
                _spec["template"] = self.template

    # End of generated code