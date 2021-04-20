rom ocp_resources.resource import NamespacedResource
from ocp_resources.utils import LOGGER, TimeoutExpiredError, TimeoutSampler


class MTV:
    """
    Abstract Class for all Migration ToolKit For Virtualization Resources included in this Module:
        Provider
        Plan (wip)
        StorageMap (wip)
        NetworkMap (wip)
        Migration (wip)
    """

    def __init__(self):
        if self.__class__.__name__ == "MTV":
            raise TypeError("MTV is not a Resource.Please Use one of it's successors.")

    def wait_for_resource_status(
        self,
        condition_status="any",
        condition_type="any",
        condition_message="any",
        condition_reason="any",
        condition_category="any",
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
            f"Wait for {self.kind} {self.name} to be "
            f"condition status:{condition_status} "
            f"condition_type: {condition_type} "
            f"condition_message: {condition_message} "
            f"condition_reason: {condition_reason} "
            f"condition_category: {condition_category}"
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
                current_conditions = sample.items[0].status.get("conditions")
                if current_conditions:
                    for condition in current_conditions:
                        last_condition = condition
                        if (condition_status  in [condition.status, "any"]
                            and condition_type in [condition.type, "any"]
                            and condition_message in [condition.message, "any"]
                            and condition_reason in [condition.reason, "any"]
                            and condition_category in [condition.category, "any"]
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

    def wait_for_condition_ready(self):
        self.wait_for_resource_status(
            condition_message=Provider.StatusConditions.MESSAGE.READY,
            condition_status=NamespacedResource.Condition.Status.TRUE,
        )
