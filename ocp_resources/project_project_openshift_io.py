# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, List, Optional
from ocp_resources.resource import Resource


class Project(Resource):
    """
        Projects are the unit of isolation and collaboration in OpenShift. A project has one or more members, a quota on the resources that the project may consume, and the security controls on the resources in the project. Within a project, members may have different roles - project administrators can set membership, editors can create and manage the resources, and viewers can see but not access running containers. In a normal cluster project administrators are not able to alter their quotas - that is restricted to cluster administrators.

    Listing or watching projects will return only projects the user has the reader role on.

    An OpenShift project is an alternative representation of a Kubernetes namespace. Projects are exposed as editable to end users while namespaces are not. Direct creation of a project is typically restricted to administrators, while end users should use the requestproject resource.

    Compatibility level 1: Stable within a major release for a minimum of 12 months or 3 minor releases (whichever is longer).
    """

    api_group: str = Resource.ApiGroup.PROJECT_OPENSHIFT_IO

    def __init__(
        self,
        finalizers: Optional[List[Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            finalizers (List[Any]): Finalizers is an opaque list of values that must be empty to
              permanently remove object from storage

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
