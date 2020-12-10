import logging

from .resource import NamespacedResource


LOGGER = logging.getLogger(__name__)


class Plan(NamespacedResource):
    """
    Plan Resource
    https://github.com/konveyor/forklift-controller/blob/master/config/crds/forklift_v1alpha1_plan.yaml
    """

    api_version = f"{NamespacedResource.ApiGroup.VIRT_KONVEYOR_IO}/{NamespacedResource.ApiVersion.V1ALPHA1}"

    def __init__(
        self,
        name,
        namespace,
        source_provider_name,
        source_provider_namespace,
        target_provider_name,
        target_provider_namespace,
        map,
        vms,
        teardown=True,
    ):
        super().__init__(name=name, namespace=namespace, teardown=teardown)
        self.source_provider_name = (source_provider_name,)
        self.source_provider_namespace = (source_provider_namespace,)
        self.target_provider_name = (target_provider_name,)
        self.target_provider_namespace = (target_provider_namespace,)
        self.map = (map,)
        self.vms = vms

    def to_dict(self):
        res = super()._base_body()
        res.update("spec", {"map": self.map, "vms": self.vms})
