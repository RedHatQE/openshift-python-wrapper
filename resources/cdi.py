from .resource import NamespacedResource


class CDI(NamespacedResource):
    """
    CDI object.
    """

    api_group = "cdi.kubevirt.io"

    class Status(NamespacedResource.Status):
        DEPLOYING = "Deploying"
        DEPLOYED = "Deployed"
