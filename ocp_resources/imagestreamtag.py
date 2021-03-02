from ocp_resources.resource import NamespacedResource


class ImageStreamTag(NamespacedResource):
    """
    ImageStreamTag object.
    """

    api_group = NamespacedResource.ApiGroup.IMAGE_OPENSHIFT_IO
