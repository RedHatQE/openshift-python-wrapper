from typing import Any, Optional

from ocp_resources.constants import NOT_FOUND_ERROR_EXCEPTION_DICT
from ocp_resources.resource import NamespacedResource
from timeout_sampler import TimeoutSampler


class Benchmark(NamespacedResource):
    """
    Benchmark resource
    Defined by https://github.com/cloud-bulldozer/benchmark-operator

    The benchmark-operator monitors a namespace for `Benchmark` resources.
    When a new `Benchmark` is created, the benchmark-operator creates and starts the pods or VMs necessary,
    and triggers the benchmark run.
    """

    api_group = NamespacedResource.ApiGroup.RIPSAW_CLOUDBULLDOZER_IO

    class Status:
        NONE: str = "None"  # None state is valid for newly created benchmark resources

    class Workload:
        class Kind:
            VM: str = "vm"
            POD: str = "pod"

    def _wait_for_instance_key(self, parent: str, key: str) -> Any:
        """
        Wait for key to exist in parent attribute of instance

        Args:
            parent (str): An attribute of `self.instance` that should contain key.
            key (str): A dictionary entry within parent

        Returns:
            Any: Value of key if found, otherwise None
        """
        samples = TimeoutSampler(
            wait_timeout=30,
            sleep=1,
            func=lambda: getattr(self.instance, parent, None),
            exceptions_dict=NOT_FOUND_ERROR_EXCEPTION_DICT,
        )
        for sample in samples:
            if sample:
                return sample.get(key)

    @property
    def uuid(self) -> str:
        """
        Returns:
            str: UUID string from resource instance
        """
        return self._wait_for_instance_key(parent="status", key="uuid")

    @property
    def suuid(self) -> str:
        """
        Returns:
            str: (short)UUID string from resource instance
        """
        return self._wait_for_instance_key(parent="status", key="suuid")

    @property
    def workload_kind(self) -> str:
        """
        Retrieve the value of spec.workload.args.kind

        Not all Benchmarks have a 'kind' defined, this was added for vms. The default is 'pod'

        Returns:
            str: Value representing workload kind

        """
        return self.workload_arg(arg="kind", default="pod")

    def workload_arg(self, arg: str, default: Optional[Any] = None) -> Any:
        """
        Retrieve the value of spec.workload.args[arg]

        To provide a similar usage as .get(), a default can be defined if needed.

        Args:
            arg (str): Argument to retrieve from spec.workload.args
            default (Any): Default value to return if arg is not found in workload args

        Returns:
            Any: Value of workload arg or 'default' if workload arg does not exist
        """
        if (workload := self._wait_for_instance_key(parent="spec", key="workload")) and isinstance(workload, dict):
            return workload.get("args", {}).get(arg, default)
        return default
