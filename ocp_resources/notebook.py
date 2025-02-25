# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from __future__ import annotations

from typing import Any
from ocp_resources.resource import NamespacedResource


class Notebook(NamespacedResource):
    """Notebook is the CR for Kubeflow Notebooks 1.x (and OpenShift AI Workbenches)."""

    api_group: str = NamespacedResource.ApiGroup.KUBEFLOW_ORG

    def __init__(
        self,
        template: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            template (dict[str, Any]): Pod template for the notebook pod.
        """
        super().__init__(**kwargs)

        self.template = template

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.template is not None:
                _spec["template"] = self.template

    # End of generated code
