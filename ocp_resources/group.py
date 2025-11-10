# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import MissingRequiredArgumentError, Resource


class Group(Resource):
    """
        Group represents a referenceable set of Users

    Compatibility level 1: Stable within a major release for a minimum of 12 months or 3 minor releases (whichever is longer).
    """

    api_group: str = Resource.ApiGroup.USER_OPENSHIFT_IO

    def __init__(
        self,
        users: list[Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            users (list[Any]): Users is the list of users in this group.

        """
        super().__init__(**kwargs)

        self.users = users

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.users is None:
                raise MissingRequiredArgumentError(argument="self.users")

            self.res["users"] = self.users

    # End of generated code
