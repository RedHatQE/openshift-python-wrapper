# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any

from ocp_resources.project_project_openshift_io import Project
from ocp_resources.resource import Resource


class ProjectRequest(Resource):
    """
        ProjectRequest is the set of options necessary to fully qualify a project request

    Compatibility level 1: Stable within a major release for a minimum of 12 months or 3 minor releases (whichever is longer).
    """

    api_group: str = Resource.ApiGroup.PROJECT_OPENSHIFT_IO

    def __init__(
        self,
        description: str | None = None,
        display_name: str | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
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
            if self.description is not None:
                self.res["description"] = self.description

            if self.display_name is not None:
                self.res["displayName"] = self.display_name

    # End of generated code

    def deploy(self, wait: bool = False) -> Project:  # type: ignore[override]
        super().deploy(wait=wait)

        project = Project(
            name=self.name,
            client=self.client,
            teardown=self.teardown,
            delete_timeout=self.delete_timeout,
        )
        project.wait_for_status(status=project.Status.ACTIVE)

        return project

    def clean_up(self, wait: bool = True, timeout: int | None = None) -> bool:
        return Project(name=self.name, client=self.client).clean_up(wait=wait, timeout=timeout)
