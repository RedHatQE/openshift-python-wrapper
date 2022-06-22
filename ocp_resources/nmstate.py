from ocp_resources.resource import NamespacedResource


class NMState(NamespacedResource):
    """
    NMState, a CR of the standalone k8s-nmstate
    """

    api_group = NamespacedResource.ApiGroup.NMSTATE_IO
