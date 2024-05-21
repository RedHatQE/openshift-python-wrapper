from ocp_resources.resource import MissingRequiredArgumentError, Resource


class ImageContentSourcePolicy(Resource):
    """
    ICSP object, inherited from Resource.
    """

    api_group = Resource.ApiGroup.OPERATOR_OPENSHIFT_IO

    def __init__(self, repository_digest_mirrors=None, **kwargs):
        """
        Create/Manage ICSP configuration object. API reference:
        https://docs.openshift.com/container-platform/4.12/rest_api/operator_apis/imagecontentsourcepolicy-operator-openshift-io-v1alpha1.html

        Args:
            repository_digest_mirrors (list of dict):
                e.g. [{source: <str>, mirrors: <list>}, ..., {source: <str>, mirrors: <list>}]
            - source - the repository that users refer to, e.g. in image pull specifications
            - mirrors - one or more repositories (str) that may also contain the same images. The order
                of mirrors in this list is treated as the user’s desired priority
        """
        self.repository_digest_mirrors = repository_digest_mirrors
        super().__init__(**kwargs)

    def to_dict(self) -> None:
        super().to_dict()
        if not self.yaml_file:
            if not self.repository_digest_mirrors:
                raise MissingRequiredArgumentError(argument="repository_digest_mirrors")
            self.res["spec"] = {"repositoryDigestMirrors": self.repository_digest_mirrors}
