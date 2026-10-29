# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md

from datetime import datetime, timezone
from typing import Any

import kubernetes
from timeout_sampler import TimeoutSampler

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.resource import NamespacedResource
from ocp_resources.utils.constants import PROTOCOL_ERROR_EXCEPTION_DICT, TIMEOUT_4MINUTES


class DaemonSet(NamespacedResource):
    """
    DaemonSet represents the configuration of a daemon set.
    """

    api_group: str = NamespacedResource.ApiGroup.APPS

    def __init__(
        self,
        min_ready_seconds: int | None = None,
        revision_history_limit: int | None = None,
        selector: dict[str, Any] | None = None,
        template: dict[str, Any] | None = None,
        update_strategy: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            min_ready_seconds (int): The minimum number of seconds for which a newly created DaemonSet pod
              should be ready without any of its container crashing, for it to
              be considered available. Defaults to 0 (pod will be considered
              available as soon as it is ready).

            revision_history_limit (int): The number of old history to retain to allow rollback. This is a
              pointer to distinguish between explicit zero and not specified.
              Defaults to 10.

            selector (dict[str, Any]): A label selector is a label query over a set of resources. The result
              of matchLabels and matchExpressions are ANDed. An empty label
              selector matches all objects. A null label selector matches no
              objects.

            template (dict[str, Any]): PodTemplateSpec describes the data a pod should have when created from
              a template

            update_strategy (dict[str, Any]): DaemonSetUpdateStrategy is a struct used to control the update
              strategy for a DaemonSet.

        """
        super().__init__(**kwargs)

        self.min_ready_seconds = min_ready_seconds
        self.revision_history_limit = revision_history_limit
        self.selector = selector
        self.template = template
        self.update_strategy = update_strategy

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.selector is None:
                raise MissingRequiredArgumentError(argument="self.selector")

            if self.template is None:
                raise MissingRequiredArgumentError(argument="self.template")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["selector"] = self.selector
            _spec["template"] = self.template

            if self.min_ready_seconds is not None:
                _spec["minReadySeconds"] = self.min_ready_seconds

            if self.revision_history_limit is not None:
                _spec["revisionHistoryLimit"] = self.revision_history_limit

            if self.update_strategy is not None:
                _spec["updateStrategy"] = self.update_strategy

    # End of generated code

    def wait_until_deployed(self, timeout: int = TIMEOUT_4MINUTES) -> None:
        """
        Wait until all Pods are deployed and ready.

        Args:
            timeout (int): Time to wait for the Daemonset.

        Raises:
            TimeoutExpiredError: If not all the pods are deployed.
        """
        self.logger.info(f"Wait for {self.kind} {self.name} to deploy all desired pods")
        samples = TimeoutSampler(
            wait_timeout=timeout,
            sleep=1,
            exceptions_dict=PROTOCOL_ERROR_EXCEPTION_DICT,
            func=lambda: self.instance,
        )
        for sample in samples:
            if sample:
                status = sample.status
                if (desired_number_scheduled := status.desiredNumberScheduled) is not None:
                    if desired_number_scheduled > 0 and desired_number_scheduled == status.numberReady:
                        return

    def delete(self, wait: bool = False, timeout: int = TIMEOUT_4MINUTES, _body: Any = None) -> bool:
        """
        Delete Daemonset.

        Uses Foreground propagation to ensure all Pods are deleted before the DaemonSet
        is removed. Without it, delete(wait=True) could return while Pods are still running.

        Args:
            wait (bool): True to wait for Daemonset to be deleted.
            timeout (int): Time to wait for resource deletion
            _body (dict): Content to send for delete()

        Returns:
            bool: True if delete succeeded, False otherwise.
        """
        return super().delete(
            wait=wait,
            timeout=timeout,
            body=kubernetes.client.V1DeleteOptions(propagation_policy="Foreground"),
        )

    def rollout(self, wait_for_rollout: bool = False, timeout: int = TIMEOUT_4MINUTES) -> None:
        """
        Restart the DaemonSet by patching the pod template with a restartedAt annotation.

        Args:
            wait_for_rollout (bool): If True, wait for the rollout to complete after restarting.
            timeout (int): Time to wait for the rollout to complete.
        """
        self.logger.info(f"Restarting {self.kind} {self.name}")
        self.update(
            resource_dict={
                "metadata": {"name": self.name},
                "spec": {
                    "template": {
                        "metadata": {
                            "annotations": {
                                "kubectl.kubernetes.io/restartedAt": datetime.now(tz=timezone.utc).isoformat()
                            }
                        }
                    }
                },
            }
        )
        if wait_for_rollout:
            self.wait_for_rollout(timeout=timeout)

    def wait_for_rollout(self, timeout: int = TIMEOUT_4MINUTES) -> None:
        """
        Wait until the DaemonSet rollout is complete.

        Checks that the controller has observed the latest generation, all pods have been
        updated, and all updated pods are available.

        Args:
            timeout (int): Time to wait for the rollout to complete.

        Raises:
            TimeoutExpiredError: If the rollout does not complete within the timeout.
        """
        self.logger.info(f"Wait for {self.kind} {self.name} rollout to complete")
        samples = TimeoutSampler(
            wait_timeout=timeout,
            sleep=1,
            exceptions_dict=PROTOCOL_ERROR_EXCEPTION_DICT,
            func=lambda: self.instance,
        )
        for sample in samples:
            if sample:
                status = sample.status
                if not status:
                    continue

                if (desired_number_scheduled := status.desiredNumberScheduled) is None:
                    continue

                if desired_number_scheduled == 0 and status.observedGeneration == sample.metadata.generation:
                    return

                if (
                    desired_number_scheduled > 0
                    and status.observedGeneration == sample.metadata.generation
                    and status.updatedNumberScheduled == desired_number_scheduled
                    and status.numberAvailable == desired_number_scheduled
                ):
                    return
