# -*- coding: utf-8 -*-
import logging

from ocp_resources.constants import PROTOCOL_ERROR_EXCEPTION_DICT
from ocp_resources.resource import TIMEOUT, NamespacedResource
from ocp_resources.utils import TimeoutSampler


LOGGER = logging.getLogger(__name__)


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
        body = super().to_dict()
        body.update({"spec": {"replicas": replica_count}})

        LOGGER.info(f"Set deployment replicas: {replica_count}")
        return self.update(resource_dict=body)

    def wait_for_replicas(self, deployed=True, timeout=TIMEOUT):
        """
        Wait until all replicas are updated.

        Args:
            deployed (bool): True for replicas deployed, False for no replicas.
            timeout (int): Time to wait for the deployment.

        Raises:
            TimeoutExpiredError: If not availableReplicas is equal to replicas.
        """
        LOGGER.info(f"Wait for {self.kind} {self.name} to be deployed: {deployed}")
        samples = TimeoutSampler(
            wait_timeout=timeout,
            sleep=1,
            exceptions_dict=PROTOCOL_ERROR_EXCEPTION_DICT,
            func=self.api.get,
            field_selector=f"metadata.name=={self.name}",
        )
        for sample in samples:
            if sample.items:
                status = sample.items[0].status
                if deployed:
                    if status.replicas == status.availableReplicas:
                        return
                else:
                    if not status.availableReplicas:
                        return
