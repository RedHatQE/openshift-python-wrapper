from ocp_resources.resource import NamespacedResource


class MachineSet(NamespacedResource):
    """
    MachineSet object.
    """
    api_group = NamespacedResource.ApiGroup.MACHINE_OPENSHIFT_IO

    @property
    def available_replicas(self):
        return self.instance.status.availableReplicas

    @property
    def ready_replicas(self):
        return self.instance.status.readyReplicas

    @property
    def num_of_replicas(self):
        return self.instance.status.replicas
