from ocp_resources.resource import NamespacedResource


class DataImportCron(NamespacedResource):
    """
    DataImportCron object
    """

    api_group = NamespacedResource.ApiGroup.CDI_KUBEVIRT_IO

    def __init__(
        self,
        name=None,
        namespace=None,
        client=None,
        source=None,
        schedule=None,
        managed_data_source=None,
        garbage_collect=None,
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
        self.schedule = schedule
        self.managed_data_source = managed_data_source
        self.garbage_collect = garbage_collect

    def to_dict(self):
        res = super().to_dict()
        if self.yaml_file:
            return res

        update_dict = {
            "spec": {
                "source": self.source,
                "schedule": self.schedule,
                "managedDataSource": self.managed_data_source,
            },
        }

        if self.garbage_collect is not None:
            update_dict["spec"]["garbageCollect"] = self.garbage_collect

        res.update(update_dict)

        return res
