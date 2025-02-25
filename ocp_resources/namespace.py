# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, List, Optional
from ocp_resources.resource import Resource


class Namespace(Resource):
    """
    Namespace provides a scope for Names. Use of multiple namespaces is optional.
    """

    api_version: str = Resource.ApiVersion.V1

    def __init__(
        self,
        finalizers: Optional[List[Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            finalizers (List[Any]): Finalizers is an opaque list of values that must be empty to
              permanently remove object from storage. More info:
              https://kubernetes.io/docs/tasks/administer-cluster/namespaces/

        """
        super().__init__(**kwargs)

        self.finalizers = finalizers

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.finalizers:
                _spec["finalizers"] = self.finalizers

    # End of generated code
