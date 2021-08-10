from ocp_resources.resource import Resource


class Infrastructure(Resource):
    """
    Infrastructure object.
    """

    api_group = Resource.ApiGroup.CONFIG_OPENSHIFT_IO

    class Type:
        BARE_METAL = "BareMetal"
        AWS = "AWS"
        OPENSTACK = "OpenStack"

    @property
    def platform(self):
        return self.instance.status.platformStatus.type
