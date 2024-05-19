# API reference: https://github.com/kubevirt/managed-tenant-quota#virtualmachinemigrationresourcequota
# TODO: update API reference when OCP doc is available

from ocp_resources.resource import NamespacedResource


class VirtualMachineMigrationResourceQuota(NamespacedResource):
    api_group = NamespacedResource.ApiGroup.MTQ_KUBEVIRT_IO

    def __init__(
        self,
        requests_cpu=None,
        requests_memory=None,
        limits_cpu=None,
        limits_memory=None,
        **kwargs,
    ):
        """
        Create VirtualMachineMigrationResourceQuota object.

        Args:
            requests_cpu (str, optional): Additional CPU requests
            limits_cpu (str, optional): Additional CPU limits
            requests_memory (str, optional): Additional Memory requests
            limits_memory (str, optional): Additional Memory limits

        """
        super().__init__(**kwargs)
        self.requests_cpu = requests_cpu
        self.requests_memory = requests_memory
        self.limits_cpu = limits_cpu
        self.limits_memory = limits_memory

    def to_dict(self) -> None:
        super().to_dict()
        if not self.yaml_file:
            additional_resources = self.res.setdefault("spec", {}).setdefault("additionalMigrationResources", {})

            if self.requests_cpu:
                additional_resources["requests.cpu"] = self.requests_cpu
            if self.requests_memory:
                additional_resources["requests.memory"] = self.requests_memory
            if self.limits_cpu:
                additional_resources["limits.cpu"] = self.limits_cpu
            if self.limits_memory:
                additional_resources["limits.memory"] = self.limits_memory
