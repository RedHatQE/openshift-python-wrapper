from ocp_resources.resource import NamespacedResource


class OCSInitialization(NamespacedResource):
    """
    OCSInitialization object.
    """

    api_group = NamespacedResource.ApiGroup.OCS_OPENSHIFT_IO
