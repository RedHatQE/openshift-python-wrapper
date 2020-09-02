from resources.resource import Resource


class MachineConfigPool(Resource):
    api_group = "machineconfiguration.openshift.io"

    class Status(Resource.Status):
        UPDATED = "Updated"
        UPDATING = "Updating"
