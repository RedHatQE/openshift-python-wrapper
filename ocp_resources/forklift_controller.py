from ocp_resources.mtv import MTV
from ocp_resources.resource import NamespacedResource


class ForkliftController(NamespacedResource, MTV):
    """
    Migration Toolkit For Virtualization (MTV) ForkliftController Resource
    """

    api_group = NamespacedResource.ApiGroup.FORKLIFT_KONVEYOR_IO
