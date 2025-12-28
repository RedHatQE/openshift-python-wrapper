# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.resource import NamespacedResource


class MultiNamespaceVirtualMachineStorageMigrationPlan(NamespacedResource):
    """
    MultiNamespaceVirtualMachineStorageMigrationPlan is the Schema for the multinamespacevmstoragemigrationplans API
    """

    api_group: str = NamespacedResource.ApiGroup.MIGRATIONS_KUBEVIRT_IO

    def __init__(
        self,
        namespaces: list[Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            namespaces (list[Any]): The virtual machines to migrate.

        """
        super().__init__(**kwargs)

        self.namespaces = namespaces

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.namespaces is None:
                raise MissingRequiredArgumentError(argument="self.namespaces")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["namespaces"] = self.namespaces

    # End of generated code
