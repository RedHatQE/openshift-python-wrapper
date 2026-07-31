# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md


from typing import Any

from ocp_resources.resource import NamespacedResource


class LLMInferenceService(NamespacedResource):
    """
    No field description from API
    """

    api_group: str = NamespacedResource.ApiGroup.SERVING_KSERVE_IO

    def __init__(
        self,
        spec_annotations: dict[str, Any] | None = None,
        base_refs: list[Any] | None = None,
        kv_cache_offloading: dict[str, Any] | None = None,
        spec_labels: dict[str, Any] | None = None,
        model: dict[str, Any] | None = None,
        parallelism: dict[str, Any] | None = None,
        prefill: dict[str, Any] | None = None,
        replicas: int | None = None,
        router: dict[str, Any] | None = None,
        scaling: dict[str, Any] | None = None,
        storage_initializer: dict[str, Any] | None = None,
        template: dict[str, Any] | None = None,
        tracing: dict[str, Any] | None = None,
        worker: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            spec_annotations (dict[str, Any]): No field description from API

            base_refs (list[Any]): No field description from API

            kv_cache_offloading (dict[str, Any]): No field description from API

            spec_labels (dict[str, Any]): No field description from API

            model (dict[str, Any]): No field description from API

            parallelism (dict[str, Any]): No field description from API

            prefill (dict[str, Any]): No field description from API

            replicas (int): No field description from API

            router (dict[str, Any]): No field description from API

            scaling (dict[str, Any]): No field description from API

            storage_initializer (dict[str, Any]): No field description from API

            template (dict[str, Any]): No field description from API

            tracing (dict[str, Any]): No field description from API

            worker (dict[str, Any]): No field description from API

        """
        super().__init__(**kwargs)

        self.spec_annotations = spec_annotations
        self.base_refs = base_refs
        self.kv_cache_offloading = kv_cache_offloading
        self.spec_labels = spec_labels
        self.model = model
        self.parallelism = parallelism
        self.prefill = prefill
        self.replicas = replicas
        self.router = router
        self.scaling = scaling
        self.storage_initializer = storage_initializer
        self.template = template
        self.tracing = tracing
        self.worker = worker

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.spec_annotations is not None:
                _spec["annotations"] = self.spec_annotations

            if self.base_refs is not None:
                _spec["baseRefs"] = self.base_refs

            if self.kv_cache_offloading is not None:
                _spec["kvCacheOffloading"] = self.kv_cache_offloading

            if self.spec_labels is not None:
                _spec["labels"] = self.spec_labels

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

            if self.scaling is not None:
                _spec["scaling"] = self.scaling

            if self.storage_initializer is not None:
                _spec["storageInitializer"] = self.storage_initializer

            if self.template is not None:
                _spec["template"] = self.template

            if self.tracing is not None:
                _spec["tracing"] = self.tracing

            if self.worker is not None:
                _spec["worker"] = self.worker

    # End of generated code
