# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, List, Optional
from ocp_resources.resource import Resource, MissingRequiredArgumentError


class Group(Resource):
    """
        Group represents a referenceable set of Users

    Compatibility level 1: Stable within a major release for a minimum of 12 months or 3 minor releases (whichever is longer).
    """

    api_group: str = Resource.ApiGroup.USER_OPENSHIFT_IO

    def __init__(
        self,
        users: Optional[List[Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            users (List[Any]): Users is the list of users in this group.

        """
        super().__init__(**kwargs)

        self.users = users

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if not self.users:
                raise MissingRequiredArgumentError(argument="self.users")

            self.res["users"] = self.users

    # End of generated code
