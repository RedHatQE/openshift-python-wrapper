from openshift.dynamic.exceptions import ResourceNotFoundError

from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.logger import get_logger
from ocp_resources.persistent_volume_claim import PersistentVolumeClaim
from ocp_resources.resource import NamespacedResource
from ocp_resources.utils import get_resource_timeout_sampler


LOGGER = get_logger(name=__name__)


class DataSource(NamespacedResource):
    api_group = NamespacedResource.ApiGroup.CDI_KUBEVIRT_IO

    def __init__(
        self,
        name=None,
        namespace=None,
        client=None,
        source=None,
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

    def to_dict(self):
        res = super().to_dict()
        if self.yaml_file:
            return res

        res.update(
            {
                "spec": {
                    "source": self.source,
                },
            }
        )

        return res

    @property
    def pvc(self):
        data_source_pvc = self.instance.spec.source.pvc
        pvc_name = data_source_pvc.name
        pvc_namespace = data_source_pvc.namespace
        try:
            return PersistentVolumeClaim(
                client=self.client,
                name=pvc_name,
                namespace=pvc_namespace,
            )
        except ResourceNotFoundError:
            LOGGER.warning(
                f"dataSource {self.name} is pointing to a non-existing PVC, name: {pvc_name}, "
                f"namespace: {pvc_namespace}"
            )

    def wait_for_status(self, status, timeout=TIMEOUT_4MINUTES, sleep=1):
        """
        Wait for data source to be in status

        Args:
            status: Expected status: True for a Ready dataSource.
            timeout (int): Time to wait for the resource.

        Raises:
            TimeoutExpiredError: If timeout reached.
        """
        LOGGER.info(
            f"Wait for {self.kind} {self.name} status to be {'' if status else 'not '}ready"
        )
        samples = get_resource_timeout_sampler(
            resource=self, status=status, timeout=timeout, sleep=sleep
        )
        for sample in samples:
            if sample.items[0].status:
                for condition in sample.items[0].status.conditions:
                    if condition.reason == "Ready" and condition.status == status:
                        return
