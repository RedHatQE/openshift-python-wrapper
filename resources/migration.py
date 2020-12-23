import logging

from urllib3.exceptions import ProtocolError

from .resource import NamespacedResource
from .utils import TimeoutExpiredError, TimeoutSampler


LOGGER = logging.getLogger(__name__)


class Migration(NamespacedResource):
    """
    Migration object.
    Used to Initiate and hold Status of a Test Plan Run
    """

    api_version = f"{NamespacedResource.ApiGroup.FORKLIFT_KONVEYOR_IO}/{NamespacedResource.ApiVersion.V1ALPHA1}"

    class StatusConditions:
        class CATEGORY:
            REQUIRED = "Required"

        class MESSAGE:
            MIGRATION_READY = "The migration is ready."
            MIGRATION_RUNNING = "The migration id RUNNING"
            MIGRATION_SUCCEEDED = "The migration has SUCCEEDED."

        class STATUS:
            TRUE = "True"

        class TYPE:
            READY = "Ready"
            RUNNING = "Running"
            SUCCEEDED = "Succeeded"

    def __init__(self, name, namespace, plan_name, plan_namespace, teardown=True):
        super().__init__(name=name, namespace=namespace, teardown=teardown)
        self.plan_name = plan_name
        self.plan_namespace = plan_namespace

    def to_dict(self):
        res = super()._base_body()
        res.update(
            {
                "spec": {
                    "plan": {"name": self.plan_name, "namespace": self.plan_namespace},
                }
            }
        )
        return res

    def wait_for_status(
        self,
        timeout=600,
        condition_message=StatusConditions.MESSAGE.MIGRATION_SUCCEEDED,
        condition_status=StatusConditions.STATUS.TRUE,
        condition_type=StatusConditions.TYPE.SUCCEEDED,
        condition_reason=None,
        condition_category=None,
    ):
        LOGGER.info(
            f"Wait for {self.kind} {self.name} condition to be {condition_type}"
        )
        samples = TimeoutSampler(
            timeout=timeout,
            sleep=1,
            exceptions=ProtocolError,
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
                                (condition.type == condition_type)
                                and (condition.status == condition_status)
                                and (condition.message == condition_message)
                                and (
                                    condition.condition_reason == condition_reason
                                    or condition_reason is None
                                )
                                and (
                                    condition.category == condition_category
                                    or condition_category is None
                                )
                            ):
                                LOGGER.info(
                                    f"Status Conditions of {self.kind} {self.name} meet the requirements: {condition}"
                                )
                                return
                            else:
                                LOGGER.info(
                                    f"Current Status Conditions of {self.kind} {self.name} : {condition}"
                                )
        except TimeoutExpiredError:
            LOGGER.info(
                f"Last Status Conditions of {self.kind} {self.name} were: {last_condition}"
            )
            raise
