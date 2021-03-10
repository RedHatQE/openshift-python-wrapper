import logging

from ocp_resources.utils import TimeoutExpiredError, TimeoutSampler


LOGGER = logging.getLogger(__name__)


def _wait_for_resource_status(
    mtv_resource,
    condition_status,
    condition_type,
    timeout=600,
    condition_message=None,
    condition_reason=None,
    condition_category=None,
):
    LOGGER.info(
        f"Wait for {mtv_resource.kind} {mtv_resource.name} condition to be {condition_type}"
    )
    samples = TimeoutSampler(
        timeout=timeout,
        sleep=1,
        exceptions=TimeoutExpiredError,
        func=mtv_resource.api().get,
        field_selector=f"metadata.name=={mtv_resource.name}",
        namespace=mtv_resource.namespace,
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
                            condition.type == condition_type
                            and condition.status == condition_status
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
            msg=f"Last Status Conditions of {mtv_resource.kind} {mtv_resource.name} were: {last_condition}"
        )
        raise
