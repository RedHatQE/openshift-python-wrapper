from datetime import date
from typing import Any

from kubernetes.dynamic import DynamicClient

from ocp_resources.resource import NamespacedResource
from ocp_resources.utils.constants import TIMEOUT_4MINUTES


class Migration(NamespacedResource):
    """
    Migration Toolkit For Virtualization (MTV) Migration object.

    Args:
        plan_name (str): MTV Plan CR name.
        plan_namespace (str): MTV Plan CR namespace.
        cut_over (date): For Warm Migration Only. Cut Over Phase Start Date & Time.
        resume_conversion (bool): Resume only the conversion phase of a failed warm
            migration, reusing preserved PVCs from the prior disk copy.

    """

    api_group = NamespacedResource.ApiGroup.FORKLIFT_KONVEYOR_IO

    def __init__(
        self,
        name: str | None = None,
        namespace: str | None = None,
        plan_name: str | None = None,
        plan_namespace: str | None = None,
        cut_over: date | None = None,
        client: DynamicClient | None = None,
        teardown: bool = True,
        yaml_file: str | None = None,
        delete_timeout: int = TIMEOUT_4MINUTES,
        *,
        resume_conversion: bool | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            teardown=teardown,
            yaml_file=yaml_file,
            delete_timeout=delete_timeout,
            **kwargs,
        )
        self.plan_name = plan_name
        self.plan_namespace = plan_namespace
        self.cut_over = cut_over
        self.resume_conversion = resume_conversion

    def to_dict(self) -> None:
        super().to_dict()
        if not self.kind_dict and not self.yaml_file:
            self.res.update({
                "spec": {
                    "plan": {
                        "name": self.plan_name,
                        "namespace": self.plan_namespace,
                    }
                }
            })

            if self.cut_over:
                self.res["spec"]["cutover"] = self.cut_over.strftime(format="%Y-%m-%dT%H:%M:%SZ")

            if self.resume_conversion:
                self.res["spec"]["resumeConversion"] = True
