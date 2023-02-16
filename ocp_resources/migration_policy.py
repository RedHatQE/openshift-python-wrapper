from ocp_resources.resource import Resource


class MigrationPolicy(Resource):
    api_group = Resource.ApiGroup.MIGRATIONS_KUBEVIRT_IO

    def __init__(
        self,
        name=None,
        allow_auto_converge=None,
        allow_post_copy=None,
        bandwidth_per_migration=None,
        completion_timeout_per_gb=None,
        namespace_selector=None,
        vmi_selector=None,
        **kwargs,
    ):
        """
        Create MigrationPolicy object.

        Args:
            name (str): Migration Policy name
            allow_auto_converge (bool, optional)
            allow_post_copy (bool, optional)
            bandwidth_per_migration (str, optional, i.e. "1Gi")
            completion_timeout_per_gb (int, optional)
            namespace_selector (dict, optional): Dict of Namespace labels to match (e.g. {"project-owner": "redhat"})
            vmi_selector (dict, optional): Dict of VMI labels to match (e.g. {"best-vm": ""})
        """
        super().__init__(
            name=name,
            **kwargs,
        )
        self.allow_auto_converge = allow_auto_converge
        self.allow_post_copy = allow_post_copy
        self.bandwidth_per_migration = bandwidth_per_migration
        self.completion_timeout_per_gb = completion_timeout_per_gb
        self.namespace_selector = namespace_selector or {}
        self.vmi_selector = vmi_selector or {}

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file:
            spec = self.res.setdefault("spec", {})
            selectors = spec.setdefault("selectors", {})

            if self.allow_auto_converge is not None:
                self.res["spec"]["allowAutoConverge"] = self.allow_auto_converge
            if self.allow_post_copy is not None:
                self.res["spec"]["allowPostCopy"] = self.allow_post_copy
            if self.bandwidth_per_migration:
                self.res["spec"]["bandwidthPerMigration"] = self.bandwidth_per_migration
            if self.completion_timeout_per_gb:
                self.res["spec"][
                    "completionTimeoutPerGiB"
                ] = self.completion_timeout_per_gb

            if self.namespace_selector:
                selectors.setdefault("namespaceSelector", {}).setdefault(
                    "matchLabels", self.namespace_selector
                )

            if self.vmi_selector:
                selectors.setdefault("virtualMachineInstanceSelector", {}).setdefault(
                    "matchLabels", self.vmi_selector
                )
