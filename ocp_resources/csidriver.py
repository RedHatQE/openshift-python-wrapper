from ocp_resources.resource import Resource


class CSIDriver(Resource):
    """
    CSIDriver object.
    """

    api_group = Resource.ApiGroup.STORAGE_K8S_IO
