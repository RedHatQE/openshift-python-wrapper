from ocp_resources.resource import MissingRequiredArgumentError, Resource


class ImageDigestMirrorSet(Resource):
    """
    API reference:
    https://docs.openshift.com/container-platform/4.14/rest_api/config_apis/imagedigestmirrorset-config-openshift-io-v1.html
    """

    api_group = Resource.ApiGroup.CONFIG_OPENSHIFT_IO

    def __init__(self, image_digest_mirrors=None, **kwargs):
        """
        Create/Manage ImageDigestMirrorSet configuration object.

        Args:
            image_digest_mirrors (list of dict):
                e.g. [{source: <str>, mirrors: <list>}, ..., {source: <str>, mirrors: <list>}]
                - source - the repository that users refer to, e.g. in image pull specifications
                - mirrors - one or more repositories (str) that may also contain the same images. The order
                    of mirrors in this list is treated as the user’s desired priority
        """
        self.image_digest_mirrors = image_digest_mirrors
        super().__init__(**kwargs)

    def to_dict(self) -> None:
        super().to_dict()
        if not self.kind_dict and not self.yaml_file:
            if not self.image_digest_mirrors:
                raise MissingRequiredArgumentError(argument="image_digest_mirrors")
            self.res["spec"] = {"imageDigestMirrors": self.image_digest_mirrors}
