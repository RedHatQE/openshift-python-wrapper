from ocp_resources.persistent_volume_claim import PersistentVolumeClaim
from ocp_resources.resource import NamespacedResource


class DataSource(NamespacedResource):
    api_group = NamespacedResource.ApiGroup.CDI_KUBEVIRT_IO

    def __init__(
        self,
        name=None,
        namespace=None,
        client=None,
        source=None,
        teardown=True,
        yaml_file=None,
    ):
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            teardown=teardown,
            yaml_file=yaml_file,
        )
        self.source = source

    def to_dict(self):
        res = super().to_dict()
        if self.yaml_file:
            return res

        res.update(
            {
                "spec": {
                    "source": self.source,
                },
            }
        )

        return res

    @property
    def pvc(self):
        data_source_pvc = self.instance.spec.source.pvc
        return PersistentVolumeClaim.get(
            dyn_client=self.client,
            name=data_source_pvc.name,
            namespace=data_source_pvc.namespace,
        )
