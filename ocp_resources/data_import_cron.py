from ocp_resources.resource import MissingRequiredArgumentError, NamespacedResource


class DataImportCron(NamespacedResource):
    """
    https://kubevirt.io/cdi-api-reference/main/definitions.html#_v1beta1_dataimportcron
    """

    api_group = NamespacedResource.ApiGroup.CDI_KUBEVIRT_IO

    def __init__(
        self,
        image_stream=None,
        url=None,
        cert_configmap=None,
        pull_method=None,
        storage_class=None,
        size=None,
        schedule=None,
        garbage_collect=None,
        managed_data_source=None,
        imports_to_keep=None,
        bind_immediate_annotation=None,
        **kwargs,
    ):
        """
        Args:
            garbage_collect (str, optional): whether old PVCs should be cleaned up after a new PVC is imported.
                Options are "Outdated"/"Never".
            imports_to_keep (int, optional): number of import PVCs to keep when garbage collecting.
            managed_data_source(str, optional): specifies the name of the corresponding DataSource to manage.
                DataSource has to be in the same namespace.
            schedule (str, optional): specifies in cron format when and how often to look for new imports.
            storage_class (str, optional): Name of the StorageClass required by the claim.
            size (str): Size of the resources claim quantity. Format is size+size unit, for example: "5Gi".
            url (str, optional): URL is the url of the registry source (starting with the scheme: docker, oci-archive).
            cert_configmap (str, optional): CertConfigMap provides a reference to the Registry certs
            image_stream (str, optional): ImageStream is the name of image stream for import
            bind_immediate_annotation (bool, optional): when WaitForFirstConsumer is set in StorageClass and the
                DataSource should be bound immediately.
            pull_method (str): can be either "pod" or "node" (node docker cache based import)
        """
        super().__init__(**kwargs)
        self.image_stream = image_stream
        self.url = url
        self.cert_configmap = cert_configmap
        self.pull_method = pull_method
        self.storage_class = storage_class
        self.size = size
        self.schedule = schedule
        self.garbage_collect = garbage_collect
        self.managed_data_source = managed_data_source
        self.imports_to_keep = imports_to_keep
        self.bind_immediate_annotation = bind_immediate_annotation

    def to_dict(self) -> None:
        super().to_dict()
        if not self.kind_dict and not self.yaml_file:
            if self.image_stream and self.url:
                raise ValueError("imageStream and url cannot coexist")

            if not self.pull_method:
                raise MissingRequiredArgumentError(argument="pull_method")

            self.res.update({
                "spec": {
                    "template": {"spec": {"source": {"registry": {"pullMethod": self.pull_method}}}},
                }
            })
            spec = self.res["spec"]["template"]["spec"]

            if self.bind_immediate_annotation:
                self.res["metadata"].setdefault("annotations", {}).update({
                    f"{NamespacedResource.ApiGroup.CDI_KUBEVIRT_IO}/storage.bind.immediate.requested": ("true")
                })
            if self.image_stream:
                spec["source"]["registry"]["imageStream"] = self.image_stream
            if self.url:
                spec["source"]["registry"]["url"] = self.url
            if self.cert_configmap:
                spec["source"]["registry"]["certConfigMap"] = self.cert_configmap
            if self.schedule:
                self.res["spec"]["schedule"] = self.schedule
            if self.garbage_collect:
                self.res["spec"]["garbageCollect"] = self.garbage_collect
            if self.managed_data_source:
                self.res["spec"]["managedDataSource"] = self.managed_data_source
            if self.imports_to_keep:
                self.res["spec"]["importsToKeep"] = self.imports_to_keep

            storage = {}
            if self.size:
                storage["resources"] = {"requests": {"storage": self.size}}
            if self.storage_class:
                storage["storageClassName"] = self.storage_class
            if storage:
                spec["storage"] = storage
