from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.resource import NamespacedResource


class DataImportCron(NamespacedResource):
    """
    DataImportCron object.
    """

    api_group = NamespacedResource.ApiGroup.CDI_KUBEVIRT_IO

    def __init__(
        self,
        name=None,
        namespace=None,
        client=None,
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
        teardown=True,
        privileged_client=None,
        yaml_file=None,
        delete_timeout=TIMEOUT_4MINUTES,
        **kwargs,
    ):
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            teardown=teardown,
            privileged_client=privileged_client,
            yaml_file=yaml_file,
            delete_timeout=delete_timeout,
            **kwargs,
        )
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

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file:
            if self.image_stream and self.url:
                raise ValueError("imageStream and url can not coexist")

            self.res.update(
                {
                    "spec": {
                        "template": {
                            "spec": {
                                "source": {
                                    "registry": {"pullMethod": self.pull_method}
                                },
                                "storage": {
                                    "resources": {"requests": {"storage": self.size}}
                                },
                            }
                        }
                    }
                }
            )
            spec = self.res["spec"]["template"]["spec"]
            if self.bind_immediate_annotation:
                self.res["metadata"].setdefault("annotations", {}).update(
                    {
                        f"{NamespacedResource.ApiGroup.CDI_KUBEVIRT_IO}/storage.bind.immediate.requested": "true"
                    }
                )
            if self.image_stream:
                spec["source"]["registry"]["imageStream"] = self.image_stream
            if self.url:
                spec["source"]["registry"]["url"] = self.url
            if self.cert_configmap:
                spec["source"]["registry"]["certConfigMap"] = self.cert_configmap
            if self.storage_class:
                spec["storage"]["storageClassName"] = self.storage_class
            if self.schedule:
                self.res["spec"]["schedule"] = self.schedule
            if self.garbage_collect:
                self.res["spec"]["garbageCollect"] = self.garbage_collect
            if self.managed_data_source:
                self.res["spec"]["managedDataSource"] = self.managed_data_source
            if self.imports_to_keep:
                self.res["spec"]["importsToKeep"] = self.imports_to_keep
