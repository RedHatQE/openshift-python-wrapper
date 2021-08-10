from ocp_resources.resource import Resource


class Infrastructure(Resource):
    """
    ImageStreamTag object.
    """

    api_group = Resource.ApiGroup.CONFIG_OPENSHIFT_IO

    @property
    def platform(self):
        return self.instance.status.platformStatus.type
