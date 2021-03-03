from ocp_resources.resource import NamespacedResource


class CDI(NamespacedResource):
    """
    CDI object.
    """

    api_group = NamespacedResource.ApiGroup.CDI_KUBEVIRT_IO

    class Status(NamespacedResource.Status):
        DEPLOYING = "Deploying"
        DEPLOYED = "Deployed"
