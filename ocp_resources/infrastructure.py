from ocp_resources.resource import Resource


class Infrastructure(Resource):
    """
    Infrastructure object.
    """

    api_version = f"{Resource.ApiGroup.CONFIG_OPENSHIFT_IO}/v1"

    @property
    def infrastructure_name(self):
        return self.instance.status.infrastructureName
