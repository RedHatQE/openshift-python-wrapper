# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import NamespacedResource


class MigController(NamespacedResource):
    """
    MigController is the Schema for the migcontrollers API.
    """

    api_group: str = NamespacedResource.ApiGroup.MIGRATIONS_KUBEVIRT_IO

    def __init__(
        self,
        image_pull_policy: str | None = None,
        infra: dict[str, Any] | None = None,
        priority_class: str | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            image_pull_policy (str): PullPolicy describes a policy for if/when to pull a container image

            infra (dict[str, Any]): Rules on which nodes infrastructure pods will be scheduled

            priority_class (str): PriorityClass of the control plane

        """
        super().__init__(**kwargs)

        self.image_pull_policy = image_pull_policy
        self.infra = infra
        self.priority_class = priority_class

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.image_pull_policy is not None:
                _spec["imagePullPolicy"] = self.image_pull_policy

            if self.infra is not None:
                _spec["infra"] = self.infra

            if self.priority_class is not None:
                _spec["priorityClass"] = self.priority_class

    # End of generated code
