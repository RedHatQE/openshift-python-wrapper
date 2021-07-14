import logging
from ocp_resources.resource import NamespacedResource


from ocp_resources.utils import TimeoutExpiredError, TimeoutSampler


LOGGER = logging.getLogger(__name__)


def _get_status_condition_log_message(**status_condition):
    log_msg = "Waiting For: \n"
    for status_condition_name, status_condition in status_condition.items():
        log_msg += (
            f"{status_condition_name}->{status_condition} \n"
            if status_condition
            else ""
        )

    return log_msg


class MTV:
    """
    Abstract Class for all Migration ToolKit For Virtualization (MTV) Resources:
        Provider,
        Plan,
        Migration,
        StorageMap,
        NetworkMap,
        
    """
    
    api_group = NamespacedResource.ApiGroup.FORKLIFT_KONVEYOR_IO

    def __init__(self):
        if self.__class__.__name__ == "MTV":
            raise TypeError("MTV is not a Resource.Please Use one of it's successors.")

    class ConditionMessage:
        PROVIDER_READY = "The provider is ready."
        NETWORK_MAP_READY = "The network map is ready."
        STORAGE_MAP_READY = "The storage map is ready."
        PLAN_READY = "The migration plan is ready."
        PLAN_SUCCEEDED = "The plan execution has SUCCEEDED."
        MIGRATION_READY = "The migration is ready."
        MIGRATION_RUNNING = "The migration is RUNNING"
        MIGRATION_SUCCEEDED = "The migration has SUCCEEDED."

    class ProviderType:
        VSPHERE = "vsphere"
        OPENSHIFT = "openshift"
        RHV = "ovirt"

    def wait_for_resource_status(
        self,
        condition_status,
        condition_type,
        condition_message=None,
        condition_reason=None,
        condition_category=None,
        wait_timeout=600,
    ):
        """
        Wait for MTV Resource Status Conditions.
        """

        LOGGER.info(
            _get_status_condition_log_message(
                condition_status=condition_status,
                condition_type=condition_type,
                condition_message=condition_message,
                condition_reason=condition_reason,
                condition_category=condition_category,
            )
        )

        samples = TimeoutSampler(
            wait_timeout=wait_timeout,
            sleep=1,
            func=self.api().get,
            field_selector=f"metadata.name=={self.name}",
            namespace=self.namespace,
        )
        last_condition = None
        try:
            for sample in samples:
                current_conditions = (
                    sample.items[0].status.get("conditions")
                    if sample.items and sample.items[0].status
                    else []
                )
                for condition in current_conditions:
                    last_condition = condition
                    if (
                        condition_status == condition.status
                        and condition_type == condition.type
                    ):
                        if (
                            condition_message == condition.message
                            or condition_status is None
                        ):
                            if (
                                condition.reason == condition.reason
                                or condition.reason is None
                            ):
                                if (
                                    condition_category == condition.category
                                    or condition_category is None
                                ):
                                    return

        except TimeoutExpiredError:
            LOGGER.error(
                msg=f"Last Status Conditions of {self.kind} {self.name} were: {last_condition}"
            )
            raise
