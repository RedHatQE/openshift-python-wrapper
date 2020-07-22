from .resource import NamespacedResource


class ImageStreamTag(NamespacedResource):
    """
    ImageStreamTag object.
    """

    api_group = "image.openshift.io"
