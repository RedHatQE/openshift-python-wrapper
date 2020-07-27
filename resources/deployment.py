# -*- coding: utf-8 -*-
import logging

from resources.utils import TimeoutSampler
from urllib3.exceptions import ProtocolError

from .resource import TIMEOUT, NamespacedResource


LOGGER = logging.getLogger(__name__)


class Deployment(NamespacedResource):
    """
    OpenShift Deployment object.
    """

    api_group = "apps"

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

    def wait_until_no_replicas(self, timeout=TIMEOUT):
        """
        Wait until all replicas are updated.

        Args:
            timeout (int): Time to wait for the deployment.

        Returns:
            bool: True if availableReplicas is not found.
        """
        LOGGER.info(f"Wait for {self.kind} {self.name} to update replicas")
        samples = TimeoutSampler(
            timeout=timeout,
            sleep=1,
            exceptions=ProtocolError,
            func=self.api().get,
            field_selector=f"metadata.name=={self.name}",
        )
        for sample in samples:
            if sample.items:
                status = sample.items[0].status
                available_replicas = status.availableReplicas
                if not available_replicas:
                    return

    def wait_until_avail_replicas(self, timeout=TIMEOUT):
        """
        Wait until all replicas are updated.

        Args:
            timeout (int): Time to wait for the deployment.

        Raises:
            TimeoutExpiredError: If not availableReplicas is equal to replicas.
        """
        LOGGER.info(
            f"Wait for {self.kind} {self.name} to ensure availableReplicas == replicas"
        )
        samples = TimeoutSampler(
            timeout=timeout,
            sleep=1,
            exceptions=ProtocolError,
            func=self.api().get,
            field_selector=f"metadata.name=={self.name}",
        )
        for sample in samples:
            if sample.items:
                status = sample.items[0].status
                available_replicas = status.availableReplicas
                replicas = status.replicas
                if replicas == available_replicas:
                    return
