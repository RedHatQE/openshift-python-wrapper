# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import Resource


class Console(Resource):
    """
        Console holds cluster-wide configuration for the web console, including the
    logout URL, and reports the public URL of the console. The canonical name is
    `cluster`.

    Compatibility level 1: Stable within a major release for a minimum of 12 months or 3 minor releases (whichever is longer).
    """

    api_group: str = Resource.ApiGroup.CONFIG_OPENSHIFT_IO

    def __init__(
        self,
        authentication: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            authentication (dict[str, Any]): ConsoleAuthentication defines a list of optional configuration for
              console authentication.

        """
        super().__init__(**kwargs)

        self.authentication = authentication

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.authentication is not None:
                _spec["authentication"] = self.authentication

    # End of generated code
