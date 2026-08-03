# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md


from typing import Any

from ocp_resources.resource import Resource


class Kueue(Resource):
    """
    Kueue is the Schema for the kueues API
    """

    api_group: str = Resource.ApiGroup.COMPONENTS_PLATFORM_OPENDATAHUB_IO

    def __init__(
        self,
        auto_create_queues: bool | None = None,
        default_cluster_queue_name: str | None = None,
        default_local_queue_name: str | None = None,
        dev_flags: dict[str, Any] | None = None,
        management_state: str | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            auto_create_queues (bool): Controls whether the operator automatically creates default
              ClusterQueue, LocalQueue and ResourceFlavor resources in managed
              namespaces. When false (the default), the operator skips queue
              creation entirely. Only used when autoCreateQueues is true.
              Available in RHOAI >= 3.5.

            default_cluster_queue_name (str): Configures the automatically created cluster queue name.

            default_local_queue_name (str): Configures the automatically created, in the managed namespaces, local
              queue name.

            dev_flags (dict[str, Any]): Add developer fields. Available in RHOAI <= 2.x.

            management_state (str): Set to one of the following values:  - "Managed"   : the operator is
              actively managing the component and trying to keep it active.
              It will only upgrade the component if it is safe to do so  -
              "Unmanaged" : the operator is actively managing the component and
              trying to keep it active.                 It will only upgrade the
              component if it is safe to do so  - "Removed"   : the operator is
              actively managing the component and will not install it,
              or if it is installed, the operator will try to remove it

        """
        super().__init__(**kwargs)

        self.auto_create_queues = auto_create_queues
        self.default_cluster_queue_name = default_cluster_queue_name
        self.default_local_queue_name = default_local_queue_name
        self.dev_flags = dev_flags
        self.management_state = management_state

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.auto_create_queues is not None:
                _spec["autoCreateQueues"] = self.auto_create_queues

            if self.default_cluster_queue_name is not None:
                _spec["defaultClusterQueueName"] = self.default_cluster_queue_name

            if self.default_local_queue_name is not None:
                _spec["defaultLocalQueueName"] = self.default_local_queue_name

            if self.dev_flags is not None:
                _spec["devFlags"] = self.dev_flags

            if self.management_state is not None:
                _spec["managementState"] = self.management_state

    # End of generated code
