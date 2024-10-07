# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, List, Optional
from ocp_resources.resource import Resource


class ImageContentSourcePolicy(Resource):
    """
       ImageContentSourcePolicy holds cluster-wide information about how to handle registry mirror rules. When multiple policies are defined, the outcome of the behavior is defined on each field.
    Compatibility level 4: No compatibility is provided, the API can change at any point for any reason. These capabilities should not be used by applications needing long term support.
    """

    api_group: str = Resource.ApiGroup.OPERATOR_OPENSHIFT_IO

    def __init__(
        self,
        repository_digest_mirrors: Optional[List[Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            repository_digest_mirrors (List[Any]): repositoryDigestMirrors allows images referenced by image digests in
              pods to be pulled from alternative mirrored repository locations.
              The image pull specification provided to the pod will be compared
              to the source locations described in RepositoryDigestMirrors and
              the image may be pulled down from any of the mirrors in the list
              instead of the specified repository allowing administrators to
              choose a potentially faster mirror. Only image pull specifications
              that have an image digest will have this behavior applied to them
              - tags will continue to be pulled from the specified repository in
              the pull spec.   Each “source” repository is treated
              independently; configurations for different “source” repositories
              don’t interact.   When multiple policies are defined for the same
              “source” repository, the sets of defined mirrors will be merged
              together, preserving the relative order of the mirrors, if
              possible. For example, if policy A has mirrors `a, b, c` and
              policy B has mirrors `c, d, e`, the mirrors will be used in the
              order `a, b, c, d, e`.  If the orders of mirror entries conflict
              (e.g. `a, b` vs. `b, a`) the configuration is not rejected but the
              resulting order is unspecified.

        """
        super().__init__(**kwargs)

        self.repository_digest_mirrors = repository_digest_mirrors

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.repository_digest_mirrors:
                _spec["repositoryDigestMirrors"] = self.repository_digest_mirrors

    # End of generated code
