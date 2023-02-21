# -*- coding: utf-8 -*-
from ocp_resources.constants import PROTOCOL_ERROR_EXCEPTION_DICT, TIMEOUT_4MINUTES
from ocp_resources.logger import get_logger
from ocp_resources.resource import NamespacedResource
from ocp_resources.utils import TimeoutSampler


LOGGER = get_logger(name=__name__)


class StatefulSet(NamespacedResource):
    """
    StatefulSet object. API Reference:
    https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/stateful-set-v1/
    """

    api_group = NamespacedResource.ApiGroup.APPS

    def __init__(
        self,
        name=None,
        namespace=None,
        yaml_file=None,
        service_name=None,
        pod_selector=None,
        pod_template=None,
        **kwargs,
    ):
        super().__init__(name=name, namespace=namespace, yaml_file=yaml_file, **kwargs)
        self.service_name = service_name
        self.pod_selector = pod_selector
        self.pod_template = pod_template

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file:
            self.res.update(
                {
                    "spec": {
                        "serviceName": self.service_name,
                        "selector": self.pod_selector,
                        "template": self.pod_template,
                    },
                }
            )

            self.res["spec"]["template"].setdefault("metadata", {}).update(
                self.pod_selector
            )

    def scale_replicas(self, replicas: int) -> None:
        """
        Scale down/up resource replicas.

        Args:
            replicas (int): num of replicas to scale_replicas to.

        """
        super().to_dict()
        self.logger.info(
            f"Scale {self.kind} from {self.instance.status.replicas} replicas to {replicas} replicas"
        )
        self.res.update({"spec": {"replicas": replicas}})
        self.update(resource_dict=self.res)

    def wait_for_replicas(
        self, deployed: bool = True, timeout: int = TIMEOUT_4MINUTES, sleep: int = 1
    ) -> None:
        """
        Wait until all replicas are updated.

        Args:
            deployed (bool): True for replicas deployed, False for no replicas.
            timeout (int): Time to wait for the deployment.
            sleep (int): Time to wait between samples.

        Raises:
            TimeoutExpiredError: If not availableReplicas is equal to replicas.
        """
        LOGGER.info(f"Wait for {self.kind} {self.name} to be deployed: {deployed}")
        samples = TimeoutSampler(
            wait_timeout=timeout,
            sleep=sleep,
            exceptions_dict=PROTOCOL_ERROR_EXCEPTION_DICT,
            func=lambda: self.instance,
        )
        for sample in samples:
            if sample:
                status = sample.status

                spec_replicas = sample.spec.replicas
                total_replicas = status.replicas or 0
                updated_replicas = status.updatedReplicas or 0
                available_replicas = status.availableReplicas or 0
                ready_replicas = status.readyReplicas or 0
                current_replicas = status.currentReplicas or 0

                if (
                    (deployed and spec_replicas)
                    and spec_replicas
                    == updated_replicas
                    == available_replicas
                    == ready_replicas
                    == current_replicas
                ) or not (deployed or spec_replicas or total_replicas):
                    return
