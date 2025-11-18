# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import MissingRequiredArgumentError, Resource


class User(Resource):
    """
        Upon log in, every user of the system receives a User and Identity resource. Administrators may directly manipulate the attributes of the users for their own tracking, or set groups via the API. The user name is unique and is chosen based on the value provided by the identity provider - if a user already exists with the incoming name, the user name may have a number appended to it depending on the configuration of the system.

    Compatibility level 1: Stable within a major release for a minimum of 12 months or 3 minor releases (whichever is longer).
    """

    api_group: str = Resource.ApiGroup.USER_OPENSHIFT_IO

    def __init__(
        self,
        full_name: str | None = None,
        groups: list[Any] | None = None,
        identities: list[Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            full_name (str): FullName is the full name of user

            groups (list[Any]): Groups specifies group names this user is a member of. This field is
              deprecated and will be removed in a future release. Instead,
              create a Group object containing the name of this User.

            identities (list[Any]): Identities are the identities associated with this user

        """
        super().__init__(**kwargs)

        self.full_name = full_name
        self.groups = groups
        self.identities = identities

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.groups is None:
                raise MissingRequiredArgumentError(argument="self.groups")

            self.res["groups"] = self.groups

            if self.full_name is not None:
                self.res["fullName"] = self.full_name

            if self.identities is not None:
                self.res["identities"] = self.identities

    # End of generated code
