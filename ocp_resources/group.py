# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, Optional
from ocp_resources.resource import Resource, MissingRequiredArgumentError


class Group(Resource):
    """
    Group represents a referenceable set of Users
    """

    api_group: str = Resource.ApiGroup.USER_OPENSHIFT_IO

    def __init__(
        self,
        users: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            users(Dict[Any, Any]): Users is the list of users in this group.

        """
        super().__init__(**kwargs)

        self.users = users

    def to_dict(self) -> None:
        super().to_dict()

        if not self.yaml_file:
            if not all([
                self.users,
            ]):
                raise MissingRequiredArgumentError(argument="users")

            self.res["users"] = self.users
