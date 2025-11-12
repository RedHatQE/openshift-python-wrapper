# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import Resource


class AAQ(Resource):
    """
    AAQ is the AAQ Operator CRD
    """

    api_group: str = Resource.ApiGroup.AAQ_KUBEVIRT_IO

    def __init__(
        self,
        cert_config: dict[str, Any] | None = None,
        configuration: dict[str, Any] | None = None,
        image_pull_policy: str | None = None,
        infra: dict[str, Any] | None = None,
        namespace_selector: dict[str, Any] | None = None,
        priority_class: str | None = None,
        workload: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            cert_config (dict[str, Any]): certificate configuration

            configuration (dict[str, Any]): holds aaq configurations.

            image_pull_policy (str): PullPolicy describes a policy for if/when to pull a container image

            infra (dict[str, Any]): Rules on which nodes AAQ infrastructure pods will be scheduled

            namespace_selector (dict[str, Any]): namespaces where pods should be gated before scheduling Defaults to
              targeting namespaces with an "application-aware-quota/enable-
              gating" label key.

            priority_class (str): PriorityClass of the AAQ control plane

            workload (dict[str, Any]): Restrict on which nodes AAQ workload pods will be scheduled

        """
        super().__init__(**kwargs)

        self.cert_config = cert_config
        self.configuration = configuration
        self.image_pull_policy = image_pull_policy
        self.infra = infra
        self.namespace_selector = namespace_selector
        self.priority_class = priority_class
        self.workload = workload

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.cert_config is not None:
                _spec["certConfig"] = self.cert_config

            if self.configuration is not None:
                _spec["configuration"] = self.configuration

            if self.image_pull_policy is not None:
                _spec["imagePullPolicy"] = self.image_pull_policy

            if self.infra is not None:
                _spec["infra"] = self.infra

            if self.namespace_selector is not None:
                _spec["namespaceSelector"] = self.namespace_selector

            if self.priority_class is not None:
                _spec["priorityClass"] = self.priority_class

            if self.workload is not None:
                _spec["workload"] = self.workload

    # End of generated code
