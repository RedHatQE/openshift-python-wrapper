from ocp_resources.resource import NamespacedResource
from ocp_resources.utils import LOGGER, TimeoutExpiredError, TimeoutSampler


def _get_status_condition_log_message(**status_condition):
    log_msg = "Waiting For: "
    for status_condition_name, status_condition in status_condition.items():
        log_msg += f"{f'{status_condition_name}->{status_condition} ' if status_condition else ''}"

    return f"{log_msg} {'Any' if log_msg == 'Waiting For: ' else ''} Condition Status"


class MTV:
    """
    Abstract Class for all Migration ToolKit For Virtualization Resources included in this Module:
        Provider
    """

    def __init__(self):
        if self.__class__.__name__ == "MTV":
            raise TypeError("MTV is not a Resource.Please Use one of it's successors.")

    def wait_for_resource_status(
        self,
        condition_status=None,
        condition_type=None,
        condition_message=None,
        condition_reason=None,
        condition_category=None,
        wait_timeout=600,
    ):
        """
        Waits for a MTV Resource status conditions.
        To Provide Maximum Flexibility to the caller, all condition attributes may be ignored.
        Normally, the inheriting resource class should implement it's own wait_for_condition_.* method, such as:
        Provider.wait_to_condition_ready,
        Plan.wait_to_condition_running and Plan.wait_to_condition_succeeded.
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
                    sample.items[0].status.get("conditions") if sample.items else None
                )
                if current_conditions:
                    for condition in current_conditions:
                        last_condition = condition
                        if (
                            (
                                condition_status == condition.status
                                or condition_status is None
                            )
                            and (
                                condition_type == condition.type
                                or condition_type is None
                            )
                            and (
                                condition_message == condition.message
                                or condition_message is None
                            )
                            and (
                                condition_reason == condition.reason
                                or condition_reason is None
                            )
                            and (
                                condition_category == condition.category
                                or condition_category is None
                            )
                        ):
                            return

        except TimeoutExpiredError:
            LOGGER.error(
                msg=f"Last Status Conditions of {self.kind} {self.name} were: {last_condition}"
            )
            raise


class Provider(NamespacedResource, MTV):
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
        provider_type=None,
        url=None,
        secret_name=None,
        secret_namespace=None,
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
        res = super().to_dict()
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

    def wait_for_condition_ready(self):
        self.wait_for_resource_status(
            condition_message=Provider.StatusConditions.MESSAGE.READY,
            condition_status=NamespacedResource.Condition.Status.TRUE,
        )
