# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import Resource


class Node(Resource):
    """
        Node holds cluster-wide information about node specific features.

    Compatibility level 1: Stable within a major release for a minimum of 12 months or 3 minor releases (whichever is longer).
    """

    api_group: str = Resource.ApiGroup.CONFIG_OPENSHIFT_IO

    def __init__(
        self,
        cgroup_mode: str | None = None,
        worker_latency_profile: str | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            cgroup_mode (str): cgroupMode determines the cgroups version on the node

            worker_latency_profile (str): workerLatencyProfile determins the how fast the kubelet is updating
              the status and corresponding reaction of the cluster

        """
        super().__init__(**kwargs)

        self.cgroup_mode = cgroup_mode
        self.worker_latency_profile = worker_latency_profile

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.cgroup_mode is not None:
                _spec["cgroupMode"] = self.cgroup_mode

            if self.worker_latency_profile is not None:
                _spec["workerLatencyProfile"] = self.worker_latency_profile

    # End of generated code
