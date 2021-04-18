import abc

from ocp_resources.resource import NamespacedResource
from ocp_resources.utils import LOGGER, TimeoutExpiredError, TimeoutSampler


class MTV(abc.ABC):
    """
    Abstract Class for all Migration ToolKit For Virtualization Resources.
    """

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


class Provider(MTV, NamespacedResource):
    """
    Provider object.
    Used to define A Source Or A Destination Provider Such as Vsphere and OpenShift Virtualization.
    """

    class StatusConditions:
        class CATEGORY:
            REQUIRED = "Required"

        class MESSAGE:
            READY = "The provider is ready."

    class ProviderType:
        VSPHERE = "vsphere"

    api_group = NamespacedResource.ApiGroup.FORKLIFT_KONVEYOR_IO

    def __init__(
        self,
        name,
        namespace,
        provider_type,
        url,
        secret_name,
        secret_namespace,
        client=None,
        teardown=True,
    ):
        super().__init__(
            name=name, namespace=namespace, client=client, teardown=teardown
        )
        self.provider_type = provider_type
        self.url = url
        self.secret_name = secret_name
        self.secret_namespace = secret_namespace

    def to_dict(self):
        res = super()._base_body()
        res.update(
            {
                "spec": {
                    "type": self.provider_type,
                    "url": self.url,
                    "secret": {
                        "name": self.secret_name,
                        "namespace": self.secret_namespace,
                    },
                }
            }
        )

        return res

    def wait_for_ready(self):
        self.wait_for_resource_status(
            condition_message=Provider.StatusConditions.MESSAGE.READY,
            condition_status=NamespacedResource.Condition.Status.TRUE,
        )
