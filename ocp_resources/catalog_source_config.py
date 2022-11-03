from ocp_resources.constants import PROTOCOL_ERROR_EXCEPTION_DICT, TIMEOUT_4MINUTES
from ocp_resources.resource import NamespacedResource
from ocp_resources.utils import TimeoutExpiredError, TimeoutSampler


class CatalogSourceConfig(NamespacedResource):
    api_group = NamespacedResource.ApiGroup.OPERATORS_COREOS_COM

    def __init__(
        self,
        name=None,
        namespace=None,
        source=None,
        target_namespace=None,
        packages=None,
        cs_display_name=None,
        cs_publisher=None,
        client=None,
        teardown=True,
        yaml_file=None,
        delete_timeout=TIMEOUT_4MINUTES,
        **kwargs,
    ):
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            teardown=teardown,
            yaml_file=yaml_file,
            delete_timeout=delete_timeout,
            **kwargs,
        )
        self.source = source
        self.target_namespace = target_namespace
        self.packages = packages
        self.cs_display_name = cs_display_name
        self.cs_publisher = cs_publisher

    def to_dict(self):
        res = super().to_dict()
        if self.yaml_file:
            return res

        res.update(
            {
                "spec": {
                    "source": self.source,
                    "targetNamespace": self.target_namespace,
                    "packages": self.packages,
                    "csDisplayName": self.cs_display_name,
                    "csPublisher": self.cs_publisher,
                }
            }
        )

        return res

    def wait_for_csc_status(self, status, timeout=120):
        """
        Wait for CatalogSourceConfig to reach requested status.
        CatalogSourceConfig Status is found under currentPhase.phase.
        Example phase: {'message': 'The object has been successfully reconciled', 'name': 'Succeeded'}

        Raises:
            TimeoutExpiredError: If CatalogSourceConfig in not in desire status.
        """
        samples = TimeoutSampler(
            wait_timeout=timeout,
            sleep=1,
            exceptions_dict=PROTOCOL_ERROR_EXCEPTION_DICT,
            func=self.api.get,
            field_selector=f"metadata.name=={self.name}",
            namespace=self.namespace,
        )
        current_status = None
        try:
            for sample in samples:
                if sample.items:
                    sample_status = sample.items[0].status
                    if sample_status:
                        current_status = sample_status.currentPhase.phase["name"]
                        if current_status == status:
                            return

        except TimeoutExpiredError:
            if current_status:
                self.logger.error(
                    f"Status of {self.kind} {self.name} is {current_status}"
                )
            raise
