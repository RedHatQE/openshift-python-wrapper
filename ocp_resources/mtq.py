# API reference: https://github.com/kubevirt/managed-tenant-quota#readme
# TODO: update API reference when OCP doc is available

from ocp_resources.resource import Resource


class MTQ(Resource):
    """
    MTQ object.
    """

    api_group = Resource.ApiGroup.MTQ_KUBEVIRT_IO
