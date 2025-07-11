from typing import Any

from ocp_resources.resource import MissingRequiredArgumentError, NamespacedResource


class FenceAgentsRemediationTemplate(NamespacedResource):
    """
    FenceAgentsRemediationTemplate CRD for managing fencing agents in a Kubernetes cluster.
    API Reference: https://github.com/medik8s/fence-agents-remediation
    """

    api_group = NamespacedResource.ApiGroup.FENCE_AGENTS_REMEDIATION_MEDIK8S_IO

    def __init__(
        self,
        agent: str,
        remediation_strategy: str | None = None,
        retry_count: int | None = None,
        retry_interval: str | None = None,
        remediation_timeout: str | None = None,
        shared_parameters: dict[str, str] | None = None,
        node_parameters: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize a FenceAgentsRemediationTemplate object.

        Args:
            agent (str): The name of the fence agent to use.
            remediation_strategy (str, optional): The strategy to use for remediation.
            retry_count (int, optional): The number of retry attempts for the fencing operation.
            retry_interval (str, optional): The interval between retry attempts.
            remediation_timeout (str, optional): The timeout for each fencing attempt.
            shared_parameters (dict, optional): Parameters common to all nodes for the fencing agent.
            node_parameters (dict, optional): Node-specific parameters for the fencing agent.
        """
        super().__init__(**kwargs)
        self.agent = agent
        self.remediation_strategy = remediation_strategy
        self.retry_count = retry_count
        self.retry_interval = retry_interval
        self.remediation_timeout = remediation_timeout
        self.shared_parameters = shared_parameters
        self.node_parameters = node_parameters

    def to_dict(self) -> None:
        super().to_dict()
        if not self.kind_dict and not self.yaml_file:
            if not self.agent:
                raise MissingRequiredArgumentError(argument="agent")
            _spec = self.res["spec"] = {"template": {"spec": {}}}
            _spec["template"]["spec"]["agent"] = self.agent
            if self.remediation_strategy:
                _spec["template"]["spec"]["remediationStrategy"] = self.remediation_strategy
            if self.retry_count is not None:
                _spec["template"]["spec"]["retrycount"] = self.retry_count
            if self.retry_interval:
                _spec["template"]["spec"]["retryinterval"] = self.retry_interval
            if self.remediation_timeout:
                _spec["template"]["spec"]["remediation_timeout"] = self.remediation_timeout
            if self.shared_parameters:
                _spec["template"]["spec"]["sharedparameters"] = self.shared_parameters
            if self.node_parameters:
                _spec["template"]["spec"]["nodeparameters"] = self.node_parameters
