from resources.resource import Resource


class MachineConfigPool(Resource):
    api_group = Resource.ApiGroup.MACHINECONFIGURATION_OPENSHIFT_IO

    class Status(Resource.Status):
        UPDATED = "Updated"
        UPDATING = "Updating"

    def __init__(
        self, name, client=None, teardown=True,
    ):
        super().__init__(name=name, client=client, teardown=teardown)
