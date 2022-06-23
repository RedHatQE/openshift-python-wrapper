from ocp_resources.resource import Resource


class NMState(Resource):
    """
    NMState, a CR of k8s-nmstate
    """

    api_group = Resource.ApiGroup.NMSTATE_IO
