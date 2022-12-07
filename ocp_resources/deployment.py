# -*- coding: utf-8 -*-
from ocp_resources.constants import PROTOCOL_ERROR_EXCEPTION_DICT, TIMEOUT_4MINUTES
from ocp_resources.resource import NamespacedResource
from ocp_resources.utils import TimeoutSampler


class Deployment(NamespacedResource):
    """
    OpenShift Deployment object.
    """

    api_group = NamespacedResource.ApiGroup.APPS

    def scale_replicas(self, replica_count=int):
        """
        Update replicas in deployment.

        Args:
            replica_count (int): Number of replicas.

        Returns:
            Deployment is updated successfully
        """
        super().to_dict()
        self.res.update({"spec": {"replicas": replica_count}})

        self.logger.info(f"Set deployment replicas: {replica_count}")
        return self.update(resource_dict=self.res)

    def wait_for_replicas(self, deployed=True, timeout=TIMEOUT_4MINUTES):
        """
        Wait until all replicas are updated.

        Args:
            deployed (bool): True for replicas deployed, False for no replicas.
            timeout (int): Time to wait for the deployment.

        Raises:
            TimeoutExpiredError: If not availableReplicas is equal to replicas.
        """
        self.logger.info(f"Wait for {self.kind} {self.name} to be deployed: {deployed}")
        samples = TimeoutSampler(
            wait_timeout=timeout,
            sleep=1,
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

                if (
                    (deployed and spec_replicas)
                    and spec_replicas
                    == updated_replicas
                    == available_replicas
                    == ready_replicas
                ) or not (deployed or spec_replicas or total_replicas):
                    return
