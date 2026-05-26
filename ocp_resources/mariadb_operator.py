# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import NamespacedResource


class MariadbOperator(NamespacedResource):
    """
    MariadbOperator is the Schema for the mariadboperators API
    """

    api_group: str = NamespacedResource.ApiGroup.HELM_MARIADB_MMONTES_IO

    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)

    # End of generated code
