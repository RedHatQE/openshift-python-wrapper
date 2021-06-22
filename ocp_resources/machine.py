from ocp_resources.resource import NamespacedResource


class Machine(NamespacedResource):
    """
    Machine object.
    """

    api_group = NamespacedResource.ApiGroup.MACHINE_OPENSHIFT_IO

    def __init__(self, name, namespace, teardown=True, client=None):
        super().__init__(
            name=name, namespace=namespace, client=client, teardown=teardown
        )

    @property
    def cluster_name(self):
        return self.instance.metadata.labels[f"{self.api_group}/cluster-api-cluster"]

    @property
    def machine_role(self):
        return self.instance.metadata.labels[
            f"{self.api_group}/cluster-api-machine-role"
        ]

    @property
    def machine_type(self):
        return self.instance.metadata.labels[
            f"{self.api_group}/cluster-api-machine-type"
        ]

    @property
    def machineset_name(self):
        return self.instance.metadata.labels[f"{self.api_group}/cluster-api-machineset"]
