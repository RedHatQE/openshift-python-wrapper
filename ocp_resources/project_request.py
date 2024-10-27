# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Optional
from ocp_resources.resource import Resource
from ocp_resources.project_project_openshift_io import Project


class ProjectRequest(Resource):
    """
        ProjectRequest is the set of options necessary to fully qualify a project request

    Compatibility level 1: Stable within a major release for a minimum of 12 months or 3 minor releases (whichever is longer).
    """

    api_group: str = Resource.ApiGroup.PROJECT_OPENSHIFT_IO

    def __init__(
        self,
        description: Optional[str] = "",
        display_name: Optional[str] = "",
        **kwargs: Any,
    ) -> None:
        """
        Args:
            description (str): Description is the description to apply to a project

            display_name (str): DisplayName is the display name to apply to a project

        """
        super().__init__(**kwargs)

        self.description = description
        self.display_name = display_name

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.description:
                self.res["description"] = self.description

            if self.display_name:
                self.res["displayName"] = self.display_name

    # End of generated code

    def clean_up(self, wait: bool = True, timeout: Optional[int] = None) -> bool:
        return Project(name=self.name).clean_up(wait=wait, timeout=timeout)
