from ocp_resources.resource import Resource


class MachineConfigPool(Resource):
    """
    MachineConfigPool object. API reference:
    https://docs.openshift.com/container-platform/4.12/rest_api/machine_apis/machineconfigpool-machineconfiguration-openshift-io-v1.html

    Args:
        machine_config_selector (dict): Matching labels/expressions, to determine which MachineConfig objects
            to apply this MachineConfigPool object.
            For filtering based on labels, the `matchLabels` dict is used - the same way as it is used in the
                nodeSelector (see the example of node_selector_labels below).
            For filtering based on expressions, the `matchExpressions` dict is used - the same way as it is used in the
                nodeSelector (see the example of node_selector_expressions below).
        configuration (dict): Targeted MachineConfig object for the machine config pool, in the following format:
            {"name": (str), "source": <List of dicts, each representing a MachineConfig resource>}
        node_selector_labels (dict): Matching labels dict with supported selector logic.
            For example:
            matchLabels:
                component: <some component>
                matchExpressions:
                - { key: tier, operator: In, values: [cache] }
                - { key: environment, operator: NotIn, values: [dev] }
        node_selector_expressions (object): Matching expressions dict with supported selector logic.
            For example:
            matchExpressions:
            - key: <resource name>/role
              operator: In
              values:
              - value_1
              - value_2
        max_unavailable (int or str): Number/percentage of nodes that can go Unavailable during an update.
        paused (bool): Whether changes to this MachineConfigPool should be stopped.
    """

    api_group = Resource.ApiGroup.MACHINECONFIGURATION_OPENSHIFT_IO

    class Status(Resource.Status):
        UPDATED = "Updated"
        UPDATING = "Updating"

    def __init__(
        self,
        machine_config_selector=None,
        configuration=None,
        node_selector_labels=None,
        node_selector_expressions=None,
        max_unavailable=None,
        paused=None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.configuration = configuration
        self.machine_config_selector = machine_config_selector
        self.node_selector_labels = node_selector_labels
        self.node_selector_expressions = node_selector_expressions
        self.max_unavailable = max_unavailable
        self.paused = paused

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file:
            self.res.update(
                {
                    "spec": {
                        "configuration": self.configuration or {},
                    },
                },
            )

            if self.machine_config_selector:
                self.res["spec"]["machineConfigSelector"] = self.machine_config_selector

            if self.node_selector_labels or self.node_selector_expressions:
                self.res["spec"]["nodeSelector"] = {}
                if self.node_selector_labels:
                    self.res["spec"]["nodeSelector"]["matchLabels"] = self.node_selector_labels
                if self.node_selector_expressions:
                    self.res["spec"]["nodeSelector"]["matchExpressions"] = self.node_selector_expressions

            if self.max_unavailable:
                self.res["spec"]["maxUnavailable"] = self.max_unavailable

            if self.paused:
                self.res["spec"]["paused"] = self.paused
