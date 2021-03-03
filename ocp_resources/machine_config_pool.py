from ocp_resources.resource import Resource


class MachineConfigPool(Resource):
    api_group = Resource.ApiGroup.MACHINECONFIGURATION_OPENSHIFT_IO

    class Status(Resource.Status):
        UPDATED = "Updated"
        UPDATING = "Updating"
