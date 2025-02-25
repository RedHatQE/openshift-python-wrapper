# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, Optional
from ocp_resources.resource import Resource


class Project(Resource):
    """
       Project holds cluster-wide information about Project.  The canonical name is `cluster`
    Compatibility level 1: Stable within a major release for a minimum of 12 months or 3 minor releases (whichever is longer).
    """

    api_group: str = Resource.ApiGroup.CONFIG_OPENSHIFT_IO

    def __init__(
        self,
        project_request_message: Optional[str] = "",
        project_request_template: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            project_request_message (str): projectRequestMessage is the string presented to a user if they are
              unable to request a project via the projectrequest api endpoint

            project_request_template (Dict[str, Any]): projectRequestTemplate is the template to use for creating projects in
              response to projectrequest. This must point to a template in
              'openshift-config' namespace. It is optional. If it is not
              specified, a default template is used.

        """
        super().__init__(**kwargs)

        self.project_request_message = project_request_message
        self.project_request_template = project_request_template

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.project_request_message:
                _spec["projectRequestMessage"] = self.project_request_message

            if self.project_request_template:
                _spec["projectRequestTemplate"] = self.project_request_template

    # End of generated code
