# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import NamespacedResource


class LLMInferenceService(NamespacedResource):
    """ """

    api_group: str = NamespacedResource.ApiGroup.SERVING_KSERVE_IO

    def __init__(
        self,
        base_refs: list[Any] | None = None,
        model: dict[str, Any] | None = None,
        parallelism: dict[str, Any] | None = None,
        prefill: dict[str, Any] | None = None,
        replicas: int | None = None,
        router: dict[str, Any] | None = None,
        template: dict[str, Any] | None = None,
        worker: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            base_refs (list[Any]): No field description from API

            model (dict[str, Any]): No field description from API

            parallelism (dict[str, Any]): No field description from API

            prefill (dict[str, Any]): No field description from API

            replicas (int): No field description from API

            router (dict[str, Any]): No field description from API

            template (dict[str, Any]): No field description from API

            worker (dict[str, Any]): No field description from API

        """
        super().__init__(**kwargs)

        self.base_refs = base_refs
        self.model = model
        self.parallelism = parallelism
        self.prefill = prefill
        self.replicas = replicas
        self.router = router
        self.template = template
        self.worker = worker

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.base_refs is not None:
                _spec["baseRefs"] = self.base_refs

            if self.model is not None:
                _spec["model"] = self.model

            if self.parallelism is not None:
                _spec["parallelism"] = self.parallelism

            if self.prefill is not None:
                _spec["prefill"] = self.prefill

            if self.replicas is not None:
                _spec["replicas"] = self.replicas

            if self.router is not None:
                _spec["router"] = self.router

            if self.template is not None:
                _spec["template"] = self.template

            if self.worker is not None:
                _spec["worker"] = self.worker

    # End of generated code
