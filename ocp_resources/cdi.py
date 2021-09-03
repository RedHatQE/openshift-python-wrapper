from ocp_resources.resource import Resource


class CDI(Resource):
    """
    CDI object.
    """

    api_group = Resource.ApiGroup.CDI_KUBEVIRT_IO

    class Status(Resource.Status):
        DEPLOYING = "Deploying"
        DEPLOYED = "Deployed"
