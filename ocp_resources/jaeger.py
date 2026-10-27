# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md


from typing import Any

from ocp_resources.resource import NamespacedResource


class Jaeger(NamespacedResource):
    """
    No field description from API
    """

    api_group: str = NamespacedResource.ApiGroup.JAEGERTRACING_IO

    def __init__(
        self,
        affinity: dict[str, Any] | None = None,
        agent: dict[str, Any] | None = None,
        all_in_one: dict[str, Any] | None = None,
        spec_annotations: dict[str, Any] | None = None,
        collector: dict[str, Any] | None = None,
        container_security_context: dict[str, Any] | None = None,
        image_pull_policy: str | None = None,
        image_pull_secrets: list[Any] | None = None,
        ingester: dict[str, Any] | None = None,
        ingress: dict[str, Any] | None = None,
        spec_labels: dict[str, Any] | None = None,
        liveness_probe: dict[str, Any] | None = None,
        query: dict[str, Any] | None = None,
        resources: dict[str, Any] | None = None,
        sampling: dict[str, Any] | None = None,
        security_context: dict[str, Any] | None = None,
        service_account: str | None = None,
        storage: dict[str, Any] | None = None,
        strategy: str | None = None,
        tolerations: list[Any] | None = None,
        ui: dict[str, Any] | None = None,
        volume_mounts: list[Any] | None = None,
        volumes: list[Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            affinity (dict[str, Any]): No field description from API

            agent (dict[str, Any]): No field description from API

            all_in_one (dict[str, Any]): No field description from API

            spec_annotations (dict[str, Any]): No field description from API

            collector (dict[str, Any]): No field description from API

            container_security_context (dict[str, Any]): No field description from API

            image_pull_policy (str): No field description from API

            image_pull_secrets (list[Any]): No field description from API

            ingester (dict[str, Any]): No field description from API

            ingress (dict[str, Any]): No field description from API

            spec_labels (dict[str, Any]): No field description from API

            liveness_probe (dict[str, Any]): No field description from API

            query (dict[str, Any]): No field description from API

            resources (dict[str, Any]): No field description from API

            sampling (dict[str, Any]): No field description from API

            security_context (dict[str, Any]): No field description from API

            service_account (str): No field description from API

            storage (dict[str, Any]): No field description from API

            strategy (str): No field description from API

            tolerations (list[Any]): No field description from API

            ui (dict[str, Any]): No field description from API

            volume_mounts (list[Any]): No field description from API

            volumes (list[Any]): No field description from API

        """
        super().__init__(**kwargs)

        self.affinity = affinity
        self.agent = agent
        self.all_in_one = all_in_one
        self.spec_annotations = spec_annotations
        self.collector = collector
        self.container_security_context = container_security_context
        self.image_pull_policy = image_pull_policy
        self.image_pull_secrets = image_pull_secrets
        self.ingester = ingester
        self.ingress = ingress
        self.spec_labels = spec_labels
        self.liveness_probe = liveness_probe
        self.query = query
        self.resources = resources
        self.sampling = sampling
        self.security_context = security_context
        self.service_account = service_account
        self.storage = storage
        self.strategy = strategy
        self.tolerations = tolerations
        self.ui = ui
        self.volume_mounts = volume_mounts
        self.volumes = volumes

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.affinity is not None:
                _spec["affinity"] = self.affinity

            if self.agent is not None:
                _spec["agent"] = self.agent

            if self.all_in_one is not None:
                _spec["allInOne"] = self.all_in_one

            if self.spec_annotations is not None:
                _spec["annotations"] = self.spec_annotations

            if self.collector is not None:
                _spec["collector"] = self.collector

            if self.container_security_context is not None:
                _spec["containerSecurityContext"] = self.container_security_context

            if self.image_pull_policy is not None:
                _spec["imagePullPolicy"] = self.image_pull_policy

            if self.image_pull_secrets is not None:
                _spec["imagePullSecrets"] = self.image_pull_secrets

            if self.ingester is not None:
                _spec["ingester"] = self.ingester

            if self.ingress is not None:
                _spec["ingress"] = self.ingress

            if self.spec_labels is not None:
                _spec["labels"] = self.spec_labels

            if self.liveness_probe is not None:
                _spec["livenessProbe"] = self.liveness_probe

            if self.query is not None:
                _spec["query"] = self.query

            if self.resources is not None:
                _spec["resources"] = self.resources

            if self.sampling is not None:
                _spec["sampling"] = self.sampling

            if self.security_context is not None:
                _spec["securityContext"] = self.security_context

            if self.service_account is not None:
                _spec["serviceAccount"] = self.service_account

            if self.storage is not None:
                _spec["storage"] = self.storage

            if self.strategy is not None:
                _spec["strategy"] = self.strategy

            if self.tolerations is not None:
                _spec["tolerations"] = self.tolerations

            if self.ui is not None:
                _spec["ui"] = self.ui

            if self.volume_mounts is not None:
                _spec["volumeMounts"] = self.volume_mounts

            if self.volumes is not None:
                _spec["volumes"] = self.volumes

    # End of generated code
