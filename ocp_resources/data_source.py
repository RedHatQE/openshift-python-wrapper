from warnings import warn

from kubernetes.dynamic.exceptions import ResourceNotFoundError

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.persistent_volume_claim import PersistentVolumeClaim
from ocp_resources.resource import NamespacedResource
from ocp_resources.volume_snapshot import VolumeSnapshot


class DataSource(NamespacedResource):
    """
    DataSource object.

    https://kubevirt.io/cdi-api-reference/main/definitions.html#_v1beta1_datasource
    """

    api_group = NamespacedResource.ApiGroup.CDI_KUBEVIRT_IO

    def __init__(self, source=None, **kwargs):
        """
        Args:
            source (dict): The source of the data.
        """
        super().__init__(**kwargs)
        self._source = source

    def to_dict(self) -> None:
        super().to_dict()
        if not self.kind_dict and not self.yaml_file:
            if not self._source:
                raise MissingRequiredArgumentError(argument="source")

            self.res.update({"spec": {"source": self._source}})

    @property
    def pvc(self):
        warn("pvc will be deprecated in v4.16, Use source instead", DeprecationWarning, stacklevel=2)
        data_source_pvc = self.instance.spec.source.pvc
        pvc_name = data_source_pvc.name
        pvc_namespace = data_source_pvc.namespace
        try:
            return PersistentVolumeClaim(
                client=self.client,
                name=pvc_name,
                namespace=pvc_namespace,
            )
        except ResourceNotFoundError:
            self.logger.warning(
                f"dataSource {self.name} is pointing to a non-existing PVC, name:"
                f" {pvc_name}, namespace: {pvc_namespace}"
            )

    @property
    def source(self):
        instance_source = self.instance.spec.source
        ds_source = next(iter(instance_source))[0]

        if ds_source == "dataSource":
            instance_source = DataSource(
                client=self.client,
                name=instance_source[ds_source].name,
                namespace=instance_source[ds_source].namespace,
                ensure_exists=True,
            ).instance.spec.source
            ds_source = next(iter(instance_source))[0]

        source_mapping = {"pvc": PersistentVolumeClaim, "snapshot": VolumeSnapshot}

        return source_mapping[ds_source](
            client=self.client,
            name=instance_source[ds_source].name,
            namespace=instance_source[ds_source].namespace,
        )

    @source.setter
    def source(self, value):
        source_type_mapping = {"pvc": PersistentVolumeClaim, "snapshot": VolumeSnapshot}
        source_type = next((key for key, cls in source_type_mapping.items() if isinstance(value, cls)), None)
        if not source_type:
            raise ValueError(f"source must be a PersistentVolumeClaim or VolumeSnapshot, got {type(value)}")
        self._source = {source_type: {"name": value.name, "namespace": value.namespace}}
