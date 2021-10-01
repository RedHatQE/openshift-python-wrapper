import logging

from ocp_resources.constants import NOT_FOUND_ERROR_EXCEPTION_DICT
from ocp_resources.resource import NamespacedResource
from ocp_resources.utils import TimeoutSampler


LOGGER = logging.getLogger(__name__)


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
        NONE = None  # None state is valid for newly created benchmark resources

    class Workload:
        class Kind:
            VM = "vm"
            POD = "pod"

    def _wait_for_instance_key(self, parent, key):
        """
        Wait for key to exist in parent attribute of instance

        Args:
            parent (str): An attribute of self.instance that should contain key
            key (str): A dictionary entry within parent

        Returns:
            str or None: Value of key if found, otherwise None
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
    def uuid(self):
        """
        Returns:
            str: UUID string from resource instance
        """
        return self._wait_for_instance_key(parent="status", key="uuid")

    @property
    def suuid(self):
        """
        Returns:
            str: (short)UUID string from resource instance
        """
        return self._wait_for_instance_key(parent="status", key="suuid")

    @property
    def workload_kind(self):
        """
        Retrieve the value of spec.workload.args.kind

        Not all Benchmarks have a 'kind' defined, this was added for vms. The default is 'pod'

        Returns:
            str: Value representing workload kind

        """
        return self.workload_arg(arg="kind", default="pod")

    def workload_arg(self, arg, default=None):
        """
        Retrieve the value of spec.workload.args[arg]

        To provide a similar usage as .get(), a default can be defined if needed.

        Args:
            arg (str): Argument to retrieve from spec.workload.args
            default (any): Default value to return if arg is not found in workload args

        Returns:
            any: Value of workload arg or 'default' if does not exist
        """
        workload = self._wait_for_instance_key(parent="spec", key="workload")
        if workload:
            return workload.get("args", {}).get(arg, default)
        return default
