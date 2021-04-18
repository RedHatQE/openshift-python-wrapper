import abc

from ocp_resources import resource
from ocp_resources.resource import NamespacedResource
from ocp_resources.utils import LOGGER, TimeoutExpiredError, TimeoutSampler


class MTV(abc.ABC, NamespacedResource):
    """
    Abstract Class for all Migration ToolKit For Virtualization Resources.
    """

    # the super returns this MTV class name and not the inheriting runtime class as required.
    @resource.classproperty
    def kind(cls):
        return cls.__name__

    def __init__(self, name, namespace, client, teardown=600):
        super().__init__(
            name=name, namespace=namespace, client=client, teardown=teardown
        )

    def wait_for_resource_status(
        self,
        condition_status=None,
        condition_type=None,
        condition_message=None,
        condition_reason=None,
        condition_category=None,
        wait_timeout=600,
    ):
        LOGGER.info(
            f"Wait for {self.kind} {self.name} to be "
            f"condition status:{condition_status or 'any'};"
            f"condition_type: {condition_type or 'any'};"
            f"condition_message: {condition_message or 'any'};"
            f"condition_reason: {condition_reason or 'any'}; "
            f"condition_category: {condition_category or 'any'}"
        )

        samples = TimeoutSampler(
            wait_timeout=wait_timeout,
            sleep=1,
            exceptions=TimeoutExpiredError,
            func=self.api().get,
            field_selector=f"metadata.name=={self.name}",
            namespace=self.namespace,
        )
        last_condition = None
        try:
            for sample in samples:
                if sample.items:
                    sample_status = sample.items[0].status
                    if sample_status:
                        current_conditions = sample_status.conditions
                        for condition in current_conditions:
                            last_condition = condition
                            if (
                                (
                                    condition.type == condition_type
                                    or condition_type is None
                                )
                                and (
                                    condition.status == condition_status
                                    or condition.status is None
                                )
                                and (
                                    condition.message == condition_message
                                    or condition_message is None
                                )
                                and (
                                    condition.condition_reason == condition_reason
                                    or condition_reason is None
                                )
                                and (
                                    condition.category == condition_category
                                    or condition_category is None
                                )
                            ):
                                return

        except TimeoutExpiredError:
            LOGGER.error(
                msg=f"Last Status Conditions of {self.kind} {self.name} were: {last_condition}"
            )
            raise
