import logging

from urllib3.exceptions import ProtocolError

from .resource import NamespacedResource
from .utils import TimeoutExpiredError, TimeoutSampler


LOGGER = logging.getLogger(__name__)


class Plan(NamespacedResource):
    """
    Plan Resource
    Please refer to MTV CRDs:
    https://github.com/konveyor/forklift-controller/blob/master/config/crds/forklift_v1alpha1_plan.yaml
    """

    class StatusConditions:
        class CATEGORY:
            REQUIRED = "Required"

        class MESSAGE:
            PROVIDER_READY = "The migration plan is ready."

        class STATUS:
            TRUE = "True"

        class TYPE:
            READY = "Ready"

    api_version = f"{NamespacedResource.ApiGroup.FORKLIFT_KONVEYOR_IO}/{NamespacedResource.ApiVersion.V1ALPHA1}"

    def __init__(
        self,
        name,
        namespace,
        source_provider_name,
        source_provider_namespace,
        destination_provider_name,
        destination_provider_namespace,
        migration_map,
        vms,
        teardown=True,
    ):
        super().__init__(name=name, namespace=namespace, teardown=teardown)
        self.source_provider_name = source_provider_name
        self.source_provider_namespace = source_provider_namespace
        self.destination_provider_name = destination_provider_name
        self.destination_provider_namespace = destination_provider_namespace
        self.migration_map = migration_map
        self.vms = vms

    def to_dict(self):
        res = super()._base_body()
        res.update(
            {
                "spec": {
                    "map": self.migration_map,
                    "vms": self.vms,
                    "provider": {
                        "source": {
                            "name": self.source_provider_name,
                            "namespace": self.source_provider_namespace,
                        },
                        "destination": {
                            "name": self.destination_provider_name,
                            "namespace": self.destination_provider_namespace,
                        },
                    },
                }
            }
        )
        return res

    def wait_for_status(
        self,
        timeout=600,
        condition_message=StatusConditions.MESSAGE.PROVIDER_READY,
        condition_status=StatusConditions.STATUS.TRUE,
        condition_type=StatusConditions.TYPE.READY,
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
