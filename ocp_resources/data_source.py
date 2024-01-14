from kubernetes.dynamic.exceptions import ResourceNotFoundError

from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.persistent_volume_claim import PersistentVolumeClaim
from ocp_resources.resource import NamespacedResource
from ocp_resources.volume_snapshot import VolumeSnapshot


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
        self.source = source

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file:
            self.res.update({
                "spec": {
                    "source": self.source,
                },
            })

    def _get_boot_source(self, boot_source_type):
        boot_source = self.instance.spec.source.get(boot_source_type)
        if not boot_source:
            return None
        boot_source_name = boot_source.name
        boot_source_namespace = boot_source.namespace
        try:
            boot_source_object = PersistentVolumeClaim if boot_source_type == "pvc" else VolumeSnapshot
            return boot_source_object(
                client=self.client,
                name=boot_source_name,
                namespace=boot_source_namespace,
            )
        except ResourceNotFoundError:
            self.logger.warning(
                f"dataSource {self.name} is pointing to a non-existing {boot_source_type}, name:"
                f" {boot_source_name}, namespace: {boot_source_namespace}"
            )

    @property
    def pvc(self):
        return self._get_boot_source(boot_source_type="pvc")

    @property
    def snapshot(self):
        return self._get_boot_source(boot_source_type="snapshot")
