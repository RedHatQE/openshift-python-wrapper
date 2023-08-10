from ocp_resources.constants import PROTOCOL_ERROR_EXCEPTION_DICT
from ocp_resources.resource import NamespacedResource
from ocp_resources.utils import TimeoutExpiredError, TimeoutSampler


class CatalogSourceConfig(NamespacedResource):
    """
    # TODO fix
    CatalogSourceConfig is used to enable an operator present in the OperatorSource to your cluster.
    Behind the scenes, it will configure an OLM CatalogSource so that the operator can then be managed by OLM.

    operators_v1_catalogsourceconfig_crd.yaml useful info
        https://github.com/nikhil-thomas/operator-marketplace/blob/e3f737b75d60d206d15e10d7078f42358d865d10/deploy/crds/operators_v1_catalogsourceconfig_crd.yaml

     Subscription in 'OLM' API official docs:
        https://olm.operatorframework.io/docs/concepts/crds/subscription/
    """

    api_group = NamespacedResource.ApiGroup.OPERATORS_COREOS_COM

    def __init__(
        self,
        source=None,
        target_namespace=None,
        packages=None,
        cs_display_name=None,
        cs_publisher=None,
        **kwargs,
    ):
        """
        Args: #TODO complete
            source (..): ..
            target_namespace (str): The namespace where the operators will be enabled.
            packages (str): Comma separated list of operator(s) without spaces which will
                be enabled in the target namespace.
            cs_display_name (str): DisplayName is passed along to the CatalogSource to be used as a pretty name.
            cs_publisher (str): Represents the entity that published the operator(s) from the OperatorSource and
                specified in packages.
        """
        if not packages:
            raise ValueError("packages can't be None")
        elif not target_namespace:
            raise ValueError("target_namespace can't be None")

        super().__init__(**kwargs)
        self.source = source
        self.target_namespace = target_namespace
        self.packages = packages
        self.cs_display_name = cs_display_name
        self.cs_publisher = cs_publisher

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file:
            self.res.update(
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
