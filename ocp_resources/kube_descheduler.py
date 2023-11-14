from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.resource import NamespacedResource


class KubeDescheduler(NamespacedResource):
    api_group = NamespacedResource.ApiGroup.OPERATOR_OPENSHIFT_IO

    def __init__(
        self,
        name=None,
        namespace=None,
        profiles=None,
        descheduling_interval=3600,
        log_level="Normal",
        management_state="Managed",
        mode="Predictive",
        operator_log_level="Normal",
        teardown=True,
        client=None,
        yaml_file=None,
        delete_timeout=TIMEOUT_4MINUTES,
        **kwargs,
    ):
        """
        Create Descheduler object.

        Args:
            profiles (list): list of descheduling profiles. Supported:
                - AffinityAndTaints
                - TopologyAndDuplicates
                - LifecycleAndUtilization
            log_level (str): logging of a component. Supported: "Normal", "Debug", "Trace", "TraceAll"
            operator_log_level (str): logging of an operator. Supported: "Normal", "Debug", "Trace", "TraceAll"
        """
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            teardown=teardown,
            yaml_file=yaml_file,
            delete_timeout=delete_timeout,
            **kwargs,
        )
        self.profiles = profiles or ["AffinityAndTaints"]
        self.descheduling_interval = descheduling_interval
        self.log_level = log_level
        self.management_state = management_state
        self.mode = mode
        self.operator_log_level = operator_log_level

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file:
            self.res.update(
                {
                    "spec": {
                        "deschedulingIntervalSeconds": self.descheduling_interval,
                        "logLevel": self.log_level,
                        "managementState": self.management_state,
                        "mode": self.mode,
                        "operatorLogLevel": self.operator_log_level,
                        "profiles": self.profiles,
                    }
                }
            )
