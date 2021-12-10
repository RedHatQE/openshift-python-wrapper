from ocp_resources.resource import NamespacedResource


class ImageStream(NamespacedResource):
    """
    ImageStream object.
    """

    api_group = NamespacedResource.ApiGroup.IMAGE_OPENSHIFT_IO
