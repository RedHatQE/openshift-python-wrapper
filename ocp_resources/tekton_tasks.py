from ocp_resources.resource import NamespacedResource


class TektonTasks(NamespacedResource):
    """
    TektonTasks object, inherited from NamespacedResource.
    """

    api_group = NamespacedResource.ApiGroup.TEKTONTASKS_KUBEVIRT_IO
