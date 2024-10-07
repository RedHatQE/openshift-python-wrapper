from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.resource import NamespacedResource


class HyperConverged(NamespacedResource):
    api_group = NamespacedResource.ApiGroup.HCO_KUBEVIRT_IO

    def __init__(
        self,
        name=None,
        namespace=None,
        client=None,
        infra=None,
        workloads=None,
        teardown=True,
        yaml_file=None,
        delete_timeout=TIMEOUT_4MINUTES,
        **kwargs,
    ):
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            teardown=teardown,
            yaml_file=yaml_file,
            delete_timeout=delete_timeout,
            **kwargs,
        )
        self.infra = infra
        self.workloads = workloads

    def to_dict(self) -> None:
        super().to_dict()
        if not self.kind_dict and not self.yaml_file:
            if self.infra:
                self.res.setdefault("spec", {}).setdefault("infra", {}).update(self.infra)

            if self.workloads:
                self.res.setdefault("spec", {}).setdefault("workloads", {}).update(self.workloads)
