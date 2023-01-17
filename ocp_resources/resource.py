import contextlib
import json
import os
import re
import sys
from io import StringIO
from signal import SIGINT, signal

import kubernetes
import yaml
from kubernetes.dynamic.exceptions import ForbiddenError, MethodNotAllowedError
from openshift.dynamic import DynamicClient
from openshift.dynamic.exceptions import ConflictError, NotFoundError
from openshift.dynamic.resource import ResourceField
from packaging.version import Version

from ocp_resources.constants import (
    DEFAULT_CLUSTER_RETRY_EXCEPTIONS,
    NOT_FOUND_ERROR_EXCEPTION_DICT,
    PROTOCOL_ERROR_EXCEPTION_DICT,
    TIMEOUT_1MINUTE,
    TIMEOUT_4MINUTES,
)
from ocp_resources.event import Event
from ocp_resources.logger import get_logger
from ocp_resources.utils import (
    TimeoutExpiredError,
    TimeoutSampler,
    skip_existing_resource_creation_teardown,
)


LOGGER = get_logger(__name__)
MAX_SUPPORTED_API_VERSION = "v2"


def _find_supported_resource(dyn_client, api_group, kind):
    results = dyn_client.resources.search(group=api_group, kind=kind)
    sorted_results = sorted(
        results, key=lambda result: KubeAPIVersion(result.api_version), reverse=True
    )
    for result in sorted_results:
        if KubeAPIVersion(result.api_version) <= KubeAPIVersion(
            MAX_SUPPORTED_API_VERSION
        ):
            return result


def _get_api_version(dyn_client, api_group, kind):
    # Returns api_group/api_version
    res = _find_supported_resource(
        dyn_client=dyn_client, api_group=api_group, kind=kind
    )
    if not res:
        log = f"Couldn't find {kind} in {api_group} api group"
        LOGGER.warning(log)
        raise NotImplementedError(log)

    LOGGER.info(f"kind: {kind} api version: {res.group_version}")
    return res.group_version


def get_client(config_file=None, config_dict=None, context=None):
    """
    Get a kubernetes client.

    Pass either config_file or config_dict.
    If none of them are passed, client will be created from default OS kubeconfig
    (environment variable or .kube folder).

    Args:
        config_file (str): path to a kubeconfig file.
        config_dict (dict): dict with kubeconfig configuration.
        context (str): name of the context to use.

    Returns:
        DynamicClient: a kubernetes client.
    """
    if config_dict:
        return DynamicClient(
            client=kubernetes.config.new_client_from_config_dict(
                config_dict=config_dict,
                context=context,
            )
        )
    return DynamicClient(
        client=kubernetes.config.new_client_from_config(
            config_file=config_file,
            context=context,
        )
    )


def sub_resource_level(current_class, owner_class, parent_class):
    # return the name of the last class in MRO list that is not one of base
    # classes; otherwise return None
    for class_iterator in reversed(
        [
            class_iterator
            for class_iterator in current_class.mro()
            if class_iterator not in owner_class.mro()
            and issubclass(class_iterator, parent_class)
        ]
    ):
        return class_iterator.__name__


class KubeAPIVersion(Version):
    """
    Implement the Kubernetes API versioning scheme from
    https://kubernetes.io/docs/concepts/overview/kubernetes-api/#api-versioning
    """

    component_re = re.compile(r"(\d+ | [a-z]+)", re.VERBOSE)

    def __init__(self, vstring=None):
        self.vstring = vstring
        self.version = None
        super().__init__(version=vstring)

    def parse(self, vstring):
        components = [comp for comp in self.component_re.split(vstring) if comp]
        for idx, obj in enumerate(components):
            with contextlib.suppress(ValueError):
                components[idx] = int(obj)

        errmsg = f"version '{vstring}' does not conform to kubernetes api versioning guidelines"

        if (
            len(components) not in (2, 4)
            or components[0] != "v"
            or not isinstance(components[1], int)
        ):
            raise ValueError(errmsg)
        if len(components) == 4 and (
            components[2] not in ("alpha", "beta") or not isinstance(components[3], int)
        ):
            raise ValueError(errmsg)

        self.version = components

    def __str__(self):
        return self.vstring

    def __repr__(self):
        return "KubeAPIVersion ('{0}')".format(str(self))

    def _cmp(self, other):
        if isinstance(other, str):
            other = KubeAPIVersion(vstring=other)

        myver = self.version
        otherver = other.version

        for ver in myver, otherver:
            if len(ver) == 2:
                ver.extend(["zeta", 9999])

        if myver == otherver:
            return 0
        if myver < otherver:
            return -1
        if myver > otherver:
            return 1


class ClassProperty:
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, owner):
        return self.func(owner)


class ValueMismatch(Exception):
    """
    Raises when value doesn't match the class value
    """


class Resource:
    """
    Base class for API resources
    """

    api_group = None
    api_version = None
    singular_name = None
    timeout_seconds = TIMEOUT_1MINUTE

    class Status:
        SUCCEEDED = "Succeeded"
        FAILED = "Failed"
        DELETING = "Deleting"
        DEPLOYED = "Deployed"
        PENDING = "Pending"
        COMPLETED = "Completed"
        RUNNING = "Running"
        READY = "Ready"
        TERMINATING = "Terminating"
        ERROR = "Error"

    class Condition:
        UPGRADEABLE = "Upgradeable"
        AVAILABLE = "Available"
        DEGRADED = "Degraded"
        PROGRESSING = "Progressing"
        CREATED = "Created"
        RECONCILE_COMPLETE = "ReconcileComplete"
        READY = "Ready"
        FAILING = "Failing"

        class Status:
            TRUE = "True"
            FALSE = "False"
            UNKNOWN = "Unknown"

        class Phase:
            INSTALL_READY = "InstallReady"
            SUCCEEDED = "Succeeded"

        class Reason:
            ALL_REQUIREMENTS_MET = "AllRequirementsMet"
            INSTALL_SUCCEEDED = "InstallSucceeded"

    class Interface:
        class State:
            UP = "up"
            DOWN = "down"
            ABSENT = "absent"

    class ApiGroup:
        ADMISSIONREGISTRATION_K8S_IO = "admissionregistration.k8s.io"
        APIEXTENSIONS_K8S_IO = "apiextensions.k8s.io"
        APIREGISTRATION_K8S_IO = "apiregistration.k8s.io"
        APP_KUBERNETES_IO = "app.kubernetes.io"
        APPS = "apps"
        BATCH = "batch"
        CDI_KUBEVIRT_IO = "cdi.kubevirt.io"
        CLONE_KUBEVIRT_IO = "clone.kubevirt.io"
        CONFIG_OPENSHIFT_IO = "config.openshift.io"
        CONSOLE_OPENSHIFT_IO = "console.openshift.io"
        DATA_IMPORT_CRON_TEMPLATE_KUBEVIRT_IO = "dataimportcrontemplate.kubevirt.io"
        EVENTS_K8S_IO = "events.k8s.io"
        EXPORT_KUBEVIRT_IO = "export.kubevirt.io"
        FORKLIFT_KONVEYOR_IO = "forklift.konveyor.io"
        INSTANCETYPE_KUBEVIRT_IO = "instancetype.kubevirt.io"
        HCO_KUBEVIRT_IO = "hco.kubevirt.io"
        HOSTPATHPROVISIONER_KUBEVIRT_IO = "hostpathprovisioner.kubevirt.io"
        IMAGE_OPENSHIFT_IO = "image.openshift.io"
        IMAGE_REGISTRY = "registry.redhat.io"
        K8S_CNI_CNCF_IO = "k8s.cni.cncf.io"
        K8S_V1_CNI_CNCF_IO = "k8s.v1.cni.cncf.io"
        KUBERNETES_IO = "kubernetes.io"
        KUBEVIRT_IO = "kubevirt.io"
        KUBEVIRT_KUBEVIRT_IO = "kubevirt.kubevirt.io"
        LITMUS_IO = "litmuschaos.io"
        MACHINE_OPENSHIFT_IO = "machine.openshift.io"
        MACHINECONFIGURATION_OPENSHIFT_IO = "machineconfiguration.openshift.io"
        MAISTRA_IO = "maistra.io"
        METALLB_IO = "metallb.io"
        MIGRATIONS_KUBEVIRT_IO = "migrations.kubevirt.io"
        MONITORING_COREOS_COM = "monitoring.coreos.com"
        NETWORKADDONSOPERATOR_NETWORK_KUBEVIRT_IO = (
            "networkaddonsoperator.network.kubevirt.io"
        )
        NETWORKING_ISTIO_IO = "networking.istio.io"
        NETWORKING_K8S_IO = "networking.k8s.io"
        NODE_LABELLER_KUBEVIRT_IO = "node-labeller.kubevirt.io"
        NMSTATE_IO = "nmstate.io"
        NODEMAINTENANCE_KUBEVIRT_IO = "nodemaintenance.kubevirt.io"
        OPERATOR_OPENSHIFT_IO = "operator.openshift.io"
        OPERATORS_COREOS_COM = "operators.coreos.com"
        OPERATORS_OPENSHIFT_IO = "operators.openshift.io"
        OS_TEMPLATE_KUBEVIRT_IO = "os.template.kubevirt.io"
        PACKAGES_OPERATORS_COREOS_COM = "packages.operators.coreos.com"
        POLICY = "policy"
        POOL_KUBEVIRT_IO = "pool.kubevirt.io"
        PROJECT_OPENSHIFT_IO = "project.openshift.io"
        RBAC_AUTHORIZATION_K8S_IO = "rbac.authorization.k8s.io"
        REMEDIATION_MEDIK8S_IO = "remediation.medik8s.io"
        RIPSAW_CLOUDBULLDOZER_IO = "ripsaw.cloudbulldozer.io"
        ROUTE_OPENSHIFT_IO = "route.openshift.io"
        SCHEDULING_K8S_IO = "scheduling.k8s.io"
        SECURITY_ISTIO_IO = "security.istio.io"
        SECURITY_OPENSHIFT_IO = "security.openshift.io"
        SNAPSHOT_STORAGE_K8S_IO = "snapshot.storage.k8s.io"
        SNAPSHOT_KUBEVIRT_IO = "snapshot.kubevirt.io"
        SRIOVNETWORK_OPENSHIFT_IO = "sriovnetwork.openshift.io"
        SSP_KUBEVIRT_IO = "ssp.kubevirt.io"
        STORAGE_K8S_IO = "storage.k8s.io"
        STORAGECLASS_KUBERNETES_IO = "storageclass.kubernetes.io"
        SUBRESOURCES_KUBEVIRT_IO = "subresources.kubevirt.io"
        TEKTONTASKS_KUBEVIRT_IO = "tektontasks.kubevirt.io"
        TEMPLATE_KUBEVIRT_IO = "template.kubevirt.io"
        TEMPLATE_OPENSHIFT_IO = "template.openshift.io"
        UPLOAD_CDI_KUBEVIRT_IO = "upload.cdi.kubevirt.io"
        V2V_KUBEVIRT_IO = "v2v.kubevirt.io"
        VELERO_IO = "velero.io"
        VM_KUBEVIRT_IO = "vm.kubevirt.io"

    class ApiVersion:
        V1 = "v1"
        V1BETA1 = "v1beta1"
        V1ALPHA1 = "v1alpha1"
        V1ALPHA3 = "v1alpha3"

    def __init__(
        self,
        name=None,
        client=None,
        teardown=True,
        timeout=TIMEOUT_4MINUTES,
        privileged_client=None,
        yaml_file=None,
        delete_timeout=TIMEOUT_4MINUTES,
        dry_run=None,
        node_selector=None,
        node_selector_labels=None,
        config_file=None,
        context=None,
        timeout_seconds=TIMEOUT_1MINUTE,
    ):
        """
        Create an API resource

        Args:
            name (str): Resource name
            client (DynamicClient): Dynamic client for connecting to a remote cluster
            teardown (bool): Indicates if this resource would need to be deleted
            privileged_client (DynamicClient): Instance of Dynamic client
            yaml_file (str): yaml file for the resource
            delete_timeout (int): timeout associated with delete action
            dry_run (bool): dry run
            node_selector (str): node selector
            node_selector_labels (str): node selector labels
            config_file (str): Path to config file for connecting to remote cluster.
            context (str): Context name for connecting to remote cluster.
            timeout_seconds (int): timeout for a get api call, call out be terminated after this many seconds

        """
        if not self.api_group and not self.api_version:
            raise NotImplementedError(
                "Subclasses of Resource require self.api_group or self.api_version to be defined"
            )
        self.namespace = None
        self.name = name
        self.client = client
        self.privileged_client = privileged_client
        self.yaml_file = yaml_file
        self.resource_dict = None  # Filled in case yaml_file is not None
        self.config_file = config_file
        self.context = context
        if not (self.name or self.yaml_file):
            raise ValueError("name or yaml file is required")

        self.teardown = teardown
        self.timeout = timeout
        self.delete_timeout = delete_timeout
        self.dry_run = dry_run
        self.node_selector = node_selector
        self.node_selector_labels = node_selector_labels
        self.node_selector_spec = self._prepare_node_selector_spec()
        self.res = None
        self.yaml_file_contents = None
        self.initial_resource_version = None
        self.logger = get_logger(name=f"{__name__.rsplit('.')[0]} {self.kind}")
        self.timeout_seconds = timeout_seconds
        self._set_client_and_api_version()

    def _prepare_node_selector_spec(self):
        if self.node_selector:
            return {f"{self.ApiGroup.KUBERNETES_IO}/hostname": self.node_selector}
        if self.node_selector_labels:
            return self.node_selector_labels

    @ClassProperty
    def kind(cls):  # noqa: N805
        return sub_resource_level(cls, NamespacedResource, Resource)

    def _base_body(self):
        """
        Generate resource dict from yaml if self.yaml_file else return base resource dict.

        Returns:
            dict: Resource dict.
        """
        if self.yaml_file:
            if not self.yaml_file_contents:
                if isinstance(self.yaml_file, StringIO):
                    self.yaml_file_contents = self.yaml_file.read()
                else:
                    with open(self.yaml_file, "r") as stream:
                        self.yaml_file_contents = stream.read()

            self.res = yaml.safe_load(stream=self.yaml_file_contents)
            self.res.get("metadata", {}).pop("resourceVersion", None)
            self.name = self.res["metadata"]["name"]
        else:
            self.res = {
                "apiVersion": self.api_version,
                "kind": self.kind,
                "metadata": {"name": self.name},
            }

    def to_dict(self):
        """
        Generate intended dict representation of the resource.
        """
        self._base_body()

    def __enter__(self):
        signal(SIGINT, self._sigint_handler)
        return self.deploy()

    def __exit__(self, exception_type, exception_value, traceback):
        if self.teardown:
            self.clean_up()

    def _sigint_handler(self, signal_received, frame):
        self.__exit__(exception_type=None, exception_value=None, traceback=None)
        sys.exit(signal_received)

    def deploy(self, wait=False):
        """
        For debug, export REUSE_IF_RESOURCE_EXISTS to skip resource create.
        Spaces are important in the export dict

        Examples:
            To skip creation of all resources by kind:
                export REUSE_IF_RESOURCE_EXISTS="{Pod: {}}"

            To skip creation of resource by name (on all namespaces or non-namespaced resources):
                export REUSE_IF_RESOURCE_EXISTS="{Pod: {<pod-name>:}}"

            To skip creation of resource by name and namespace:
                export REUSE_IF_RESOURCE_EXISTS="{Pod: {<pod-name>: <pod-namespace>}}"

            To skip creation of multiple resources:
                export REUSE_IF_RESOURCE_EXISTS="{Namespace: {<namespace-name>:}, Pod: {<pod-name>: <pod-namespace>}}"
        """
        _resource = None
        _export_str = "REUSE_IF_RESOURCE_EXISTS"
        skip_resource_kind_create_if_exists = os.environ.get(_export_str)
        if skip_resource_kind_create_if_exists:
            _resource = skip_existing_resource_creation_teardown(
                resource=self,
                export_str=_export_str,
                user_exported_args=skip_resource_kind_create_if_exists,
            )

            if _resource:
                return _resource

        self.create(wait=wait)
        return self

    def clean_up(self):
        """
        For debug, export SKIP_RESOURCE_TEARDOWN to skip resource teardown.
        Spaces are important in the export dict

        Examples:
            To skip teardown of all resources by kind:
                export SKIP_RESOURCE_TEARDOWN="{Pod: {}}"

            To skip teardown of resource by name (on all namespaces):
                export SKIP_RESOURCE_TEARDOWN="{Pod: {<pod-name>:}}"

            To skip teardown of resource by name and namespace:
                export SKIP_RESOURCE_TEARDOWN="{Pod: {<pod-name>: <pod-namespace>}}"

            To skip teardown of multiple resources:
                export SKIP_RESOURCE_TEARDOWN="{Namespace: {<namespace-name>:}, Pod: {<pod-name>: <pod-namespace>}}"
        """
        _export_str = "SKIP_RESOURCE_TEARDOWN"
        skip_resource_teardown = os.environ.get(_export_str)
        if skip_resource_teardown and skip_existing_resource_creation_teardown(
            resource=self,
            export_str=_export_str,
            user_exported_args=skip_resource_teardown,
            check_exists=False,
        ):
            self.logger.warning(
                f"Skip resource {self.kind} {self.name} teardown. Got {_export_str}={skip_resource_teardown}"
            )
            return

        self.delete(wait=True, timeout=self.delete_timeout)

    @classmethod
    def _prepare_resources(cls, dyn_client, singular_name, *args, **kwargs):
        if not cls.api_version:
            cls.api_version = _get_api_version(
                dyn_client=dyn_client, api_group=cls.api_group, kind=cls.kind
            )

        get_kwargs = {"singular_name": singular_name} if singular_name else {}
        return dyn_client.resources.get(
            kind=cls.kind,
            api_version=cls.api_version,
            **get_kwargs,
        ).get(*args, **kwargs, timeout_seconds=cls.timeout_seconds)

    def _prepare_singular_name_kwargs(self, **kwargs):
        kwargs = kwargs if kwargs else {}
        if self.singular_name:
            kwargs["singular_name"] = self.singular_name

        return kwargs

    def _set_client_and_api_version(self):
        if not self.client:
            self.client = get_client(config_file=self.config_file, context=self.context)

        if not self.api_version:
            self.api_version = _get_api_version(
                dyn_client=self.client, api_group=self.api_group, kind=self.kind
            )

    def full_api(self, **kwargs):
        """
        Get resource API

        Keyword Args:
            pretty
            _continue
            include_uninitialized
            field_selector
            label_selector
            limit
            resource_version
            timeout_seconds
            watch
            async_req

        Returns:
            Resource: Resource object.
        """
        self._set_client_and_api_version()

        kwargs = self._prepare_singular_name_kwargs(**kwargs)

        return self.client.resources.get(
            api_version=self.api_version, kind=self.kind, **kwargs
        )

    @property
    def api(self):
        return self.full_api()

    def wait(self, timeout=TIMEOUT_4MINUTES, sleep=1):
        """
        Wait for resource

        Args:
            timeout (int): Time to wait for the resource.
            sleep (int): Time to wait between retries

        Raises:
            TimeoutExpiredError: If resource not exists.
        """
        self.logger.info(f"Wait until {self.kind} {self.name} is created")
        samples = TimeoutSampler(
            wait_timeout=timeout,
            sleep=sleep,
            exceptions_dict={
                **PROTOCOL_ERROR_EXCEPTION_DICT,
                **NOT_FOUND_ERROR_EXCEPTION_DICT,
                **DEFAULT_CLUSTER_RETRY_EXCEPTIONS,
            },
            func=lambda: self.exists,
        )
        for sample in samples:
            if sample:
                return

    def wait_deleted(self, timeout=TIMEOUT_4MINUTES):
        """
        Wait until resource is deleted

        Args:
            timeout (int): Time to wait for the resource.

        Raises:
            TimeoutExpiredError: If resource still exists.
        """
        self.logger.info(f"Wait until {self.kind} {self.name} is deleted")
        return self.client_wait_deleted(timeout=timeout)

    @property
    def exists(self):
        """
        Whether self exists on the server
        """
        try:
            return self.instance
        except NotFoundError:
            return None

    def client_wait_deleted(self, timeout):
        """
        client-side Wait until resource is deleted

        Args:
            timeout (int): Time to wait for the resource.

        Raises:
            TimeoutExpiredError: If resource still exists.
        """
        samples = TimeoutSampler(
            wait_timeout=timeout, sleep=1, func=lambda: self.exists
        )
        for sample in samples:
            if not sample:
                return

    def wait_for_status(
        self, status, timeout=TIMEOUT_4MINUTES, stop_status=None, sleep=1
    ):
        """
        Wait for resource to be in status

        Args:
            status (str): Expected status.
            timeout (int): Time to wait for the resource.
            stop_status (str): Status which should stop the wait and failed.

        Raises:
            TimeoutExpiredError: If resource in not in desire status.
        """
        stop_status = stop_status if stop_status else self.Status.FAILED
        self.logger.info(f"Wait for {self.kind} {self.name} status to be {status}")
        samples = TimeoutSampler(
            wait_timeout=timeout,
            sleep=sleep,
            exceptions_dict={
                **PROTOCOL_ERROR_EXCEPTION_DICT,
                **DEFAULT_CLUSTER_RETRY_EXCEPTIONS,
            },
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
                        current_status = sample_status.phase
                        if current_status == status:
                            return

                        if current_status == stop_status:
                            raise TimeoutExpiredError(
                                f"Status of {self.kind} {self.name} is {current_status}"
                            )

        except TimeoutExpiredError:
            if current_status:
                self.logger.error(
                    f"Status of {self.kind} {self.name} is {current_status}"
                )
            raise

    def create(self, wait=False):
        """
        Create resource.

        Args:
            wait (bool) : True to wait for resource status.

        Returns:
            bool: True if create succeeded, False otherwise.

        Raises:
            ValueMismatch: When body value doesn't match class value
        """
        if not self.res:
            self.to_dict()

        self.logger.info(f"Create {self.kind} {self.name}")
        self.logger.info(f"Posting {self.res}")
        self.logger.debug(f"\n{yaml.dump(self.res)}")
        resource_ = self.api.create(
            body=self.res, namespace=self.namespace, dry_run=self.dry_run
        )
        with contextlib.suppress(NotFoundError, ForbiddenError):
            # some resources do not support get() (no instance) or the client do not have permissions
            self.initial_resource_version = self.instance.metadata.resourceVersion

        if wait and resource_:
            return self.wait()
        return resource_

    def delete(self, wait=False, timeout=TIMEOUT_4MINUTES, body=None):
        self.logger.info(f"Delete {self.kind} {self.name}")
        if self.exists:
            data = self.instance.to_dict()
            self.logger.info(f"Deleting {data}")
            self.logger.debug(f"\n{yaml.dump(data)}")

        try:
            res = self.api.delete(name=self.name, namespace=self.namespace, body=body)
        except NotFoundError:
            return False

        if wait and res:
            return self.wait_deleted(timeout=timeout)
        return res

    @property
    def status(self):
        """
        Get resource status

        Status: Running, Scheduling, Pending, Unknown, CrashLoopBackOff

        Returns:
           str: Status
        """
        self.logger.info(f"Get {self.kind} {self.name} status")
        return self.instance.status.phase

    def update(self, resource_dict):
        """
        Update resource with resource dict

        Args:
            resource_dict: Resource dictionary
        """
        self.logger.info(f"Update {self.kind} {self.name}:\n{resource_dict}")
        self.logger.debug(f"\n{yaml.dump(resource_dict)}")
        self.api.patch(
            body=resource_dict,
            namespace=self.namespace,
            content_type="application/merge-patch+json",
        )

    def update_replace(self, resource_dict):
        """
        Replace resource metadata.
        Use this to remove existing field. (update() will only update existing fields)
        """
        self.logger.info(f"Replace {self.kind} {self.name}: \n{resource_dict}")
        self.logger.debug(f"\n{yaml.dump(resource_dict)}")
        self.api.replace(body=resource_dict, name=self.name, namespace=self.namespace)

    @staticmethod
    def retry_cluster_exceptions(
        func, exceptions_dict=DEFAULT_CLUSTER_RETRY_EXCEPTIONS, **kwargs
    ):

        sampler = TimeoutSampler(
            wait_timeout=10,
            sleep=1,
            func=func,
            print_log=False,
            exceptions_dict=exceptions_dict,
            **kwargs,
        )
        for sample in sampler:
            return sample

    @classmethod
    def get(
        cls,
        dyn_client=None,
        config_file=None,
        context=None,
        singular_name=None,
        *args,
        **kwargs,
    ):
        """
        Get resources

        Args:
            dyn_client (DynamicClient): Open connection to remote cluster.
            config_file (str): Path to config file for connecting to remote cluster.
            context (str): Context name for connecting to remote cluster.
            singular_name (str): Resource kind (in lowercase), in use where we have multiple matches for resource.

        Returns:
            generator: Generator of Resources of cls.kind
        """
        if not dyn_client:
            dyn_client = get_client(config_file=config_file, context=context)

        def _get():
            _resources = cls._prepare_resources(
                dyn_client=dyn_client, singular_name=singular_name, *args, **kwargs
            )
            try:
                for resource_field in _resources.items:
                    yield cls(client=dyn_client, name=resource_field.metadata.name)
            except TypeError:
                yield cls(client=dyn_client, name=_resources.metadata.name)

        return Resource.retry_cluster_exceptions(func=_get)

    @property
    def instance(self):
        """
        Get resource instance

        Returns:
            openshift.dynamic.client.ResourceInstance
        """

        def _instance():
            return self.api.get(name=self.name)

        return self.retry_cluster_exceptions(func=_instance)

    @property
    def labels(self):
        """
        Method to get labels for this resource

        Returns:
           openshift.dynamic.resource.ResourceField: Representation of labels
        """
        return self.instance["metadata"]["labels"]

    def watcher(self, timeout, resource_version=None):
        """
        Get resource for a given timeout.

        Args:
            timeout (int): Time to get conditions.
            resource_version (str): The version with which to filter results. Only events with
                a resource_version greater than this value will be returned

        Yield:
            Event object with these keys:
                   'type': The type of event such as "ADDED", "DELETED", etc.
                   'raw_object': a dict representing the watched object.
                   'object': A ResourceInstance wrapping raw_object.
        """
        yield from self.api.watch(
            timeout=timeout,
            namespace=self.namespace,
            field_selector=f"metadata.name=={self.name}",
            resource_version=resource_version or self.initial_resource_version,
        )

    def wait_for_condition(self, condition, status, timeout=300):
        """
        Wait for Resource condition to be in desire status.

        Args:
            condition (str): Condition to query.
            status (str): Expected condition status.
            timeout (int): Time to wait for the resource.

        Raises:
            TimeoutExpiredError: If Resource condition in not in desire status.
        """
        self.logger.info(
            f"Wait for {self.kind}/{self.name}'s '{condition}' condition to be '{status}'"
        )
        for sample in self.watcher(timeout=timeout):
            for cond in sample["raw_object"].get("status", {}).get("conditions", []):
                if cond["type"] == condition and cond["status"] == status:
                    return
        raise TimeoutExpiredError(
            value=f"condition {condition} not in desired status {status} after {timeout} seconds"
        )

    def api_request(self, method, action, url, **params):
        """
        Handle API requests to resource.

        Args:
            method (str): Request method (GET/PUT etc.).
            action (str): Action to perform (stop/start/guestosinfo etc.).
            url (str): URL of resource.

        Returns:
           data(dict): response data

        """
        client = self.privileged_client or self.client
        response = client.client.request(
            method=method,
            url=f"{url}/{action}",
            headers=self.client.configuration.api_key,
            **params,
        )

        try:
            return json.loads(response.data)
        except json.decoder.JSONDecodeError:
            return response.data

    def wait_for_conditions(self):
        samples = TimeoutSampler(
            wait_timeout=30, sleep=1, func=lambda: self.instance.status.conditions
        )
        for sample in samples:
            if sample:
                return

    def events(
        self,
        name=None,
        label_selector=None,
        field_selector=None,
        resource_version=None,
        timeout=None,
    ):
        """
        get - retrieves K8s events.

        Args:
            name (str): event name
            label_selector (str): filter events by labels; comma separated string of key=value
            field_selector (str): filter events by fields; comma separated string of key=valueevent fields;
                comma separated string of key=value
            resource_version (str): filter events by their resource's version
            timeout (int): timeout in seconds

        Returns
            list: event objects

        example: reading all CSV Warning events in namespace "my-namespace", with reason of "AnEventReason"
            pod = Pod(client=client, name="pod", namespace="my-namespace")
            for event in pod.events(
                default_client,
                namespace="my-namespace",
                field_selector="involvedObject.kind==ClusterServiceVersion,type==Warning,reason=AnEventReason",
                timeout=10,
            ):
                print(event.object)
        """
        _field_selector = f"involvedObject.name=={self.name}"
        if field_selector:
            field_selector = f"{_field_selector},{field_selector}"
        yield from Event.get(
            dyn_client=self.client,
            namespace=self.namespace,
            name=name,
            label_selector=label_selector,
            field_selector=field_selector or _field_selector,
            resource_version=resource_version,
            timeout=timeout,
        )

    @staticmethod
    def get_all_cluster_resources(
        config_file=None, config_dict=None, context=None, *args, **kwargs
    ):
        """
        Get all cluster resources

        Args:
            config_file (str): path to a kubeconfig file.
            config_dict (dict): dict with kubeconfig configuration.
            context (str): name of the context to use.
            *args (tuple): args to pass to client.get()
            **kwargs (dict): kwargs to pass to client.get()

        Yields:
            kubernetes.dynamic.resource.ResourceField: Cluster resource.

        Example:
            for resource in get_all_cluster_resources(label_selector="my-label=value"):
                print(f"Resource: {resource}")
        """

        client = get_client(
            config_file=config_file, config_dict=config_dict, context=context
        )
        for _resource in client.resources.search():
            try:
                _resources = client.get(_resource, *args, **kwargs)
                yield from _resources.items

            except (NotFoundError, TypeError, MethodNotAllowedError):
                continue

    def to_yaml(self):
        """
        Get resource as YAML representation.

        Returns:
            str: Resource YAML representation.
        """
        if not self.res:
            self.to_dict()
        resource_yaml = yaml.dump(self.res)
        self.logger.info(f"\n{resource_yaml}")
        return resource_yaml


class NamespacedResource(Resource):
    """
    Namespaced object, inherited from Resource.
    """

    def __init__(
        self,
        name=None,
        namespace=None,
        client=None,
        teardown=True,
        timeout=TIMEOUT_4MINUTES,
        privileged_client=None,
        yaml_file=None,
        delete_timeout=TIMEOUT_4MINUTES,
        **kwargs,
    ):
        super().__init__(
            name=name,
            client=client,
            teardown=teardown,
            timeout=timeout,
            privileged_client=privileged_client,
            yaml_file=yaml_file,
            delete_timeout=delete_timeout,
            **kwargs,
        )
        self.namespace = namespace
        if not (self.name and self.namespace) and not self.yaml_file:
            raise ValueError("name and namespace or yaml file is required")

    @classmethod
    def get(
        cls,
        dyn_client=None,
        config_file=None,
        context=None,
        singular_name=None,
        raw=False,
        *args,
        **kwargs,
    ):
        """
        Get resources

        Args:
            dyn_client (DynamicClient): Open connection to remote cluster
            config_file (str): Path to config file for connecting to remote cluster.
            context (str): Context name for connecting to remote cluster.
            singular_name (str): Resource kind (in lowercase), in use where we have multiple matches for resource
            raw (bool): If True return raw object from openshift-restclient-python


        Returns:
            generator: Generator of Resources of cls.kind
        """
        if not dyn_client:
            dyn_client = get_client(config_file=config_file, context=context)

        _resources = cls._prepare_resources(
            dyn_client=dyn_client, singular_name=singular_name, *args, **kwargs
        )
        try:
            for resource_field in _resources.items:
                if raw:
                    yield resource_field
                else:
                    yield cls(
                        client=dyn_client,
                        name=resource_field.metadata.name,
                        namespace=resource_field.metadata.namespace,
                    )
        except TypeError:
            if raw:
                yield _resources
            else:
                yield cls(
                    client=dyn_client,
                    name=_resources.metadata.name,
                    namespace=_resources.metadata.namespace,
                )

    @property
    def instance(self):
        """
        Get resource instance

        Returns:
            openshift.dynamic.client.ResourceInstance
        """
        return self.api.get(name=self.name, namespace=self.namespace)

    def _base_body(self):
        if not self.res:
            super(NamespacedResource, self)._base_body()

        if self.yaml_file:
            self.namespace = self.res["metadata"].get("namespace", self.namespace)

        if not self.namespace:
            raise ValueError("Namespace must be passed or specified in the YAML file.")

        if not self.yaml_file:
            self.res["metadata"]["namespace"] = self.namespace

    def to_dict(self):
        self._base_body()


class ResourceEditor:
    def __init__(self, patches, action="update", user_backups=None):
        """
        Args:
            patches (dict): {<Resource object>: <yaml patch as dict>}
                e.g. {<Resource object>:
                        {'metadata': {'labels': {'label1': 'true'}}}

        Allows for temporary edits to cluster resources for tests. During
        __enter__ user-specified patches (see args) are applied and old values
        are backed up, and during __exit__ these backups are used to reverse
        all changes made.

        Flow:
        1) apply patches
        2) automation runs
        3) edits made to resources are reversed

        May also be used without being treated as a context manager by
        calling the methods update() and restore() after instantiation.

        *** the DynamicClient object used to get the resources must not be
         using an unprivileged_user; use default_client or similar instead.***
        """

        self._patches = self._dictify_resourcefield(res=patches)
        self.action = action
        self.user_backups = user_backups
        self._backups = {}

    @property
    def backups(self):
        """Returns a dict {<Resource object>: <backup_as_dict>}
        The backup dict kept for each resource edited"""
        return self._backups

    @property
    def patches(self):
        """Returns the patches dict provided in the constructor"""
        return self._patches

    def update(self, backup_resources=False):
        """Prepares backup dicts (where necessary) and applies patches"""
        # prepare update dicts and backups
        resource_to_patch = []
        if backup_resources:
            LOGGER.info("ResourceEdit: Backing up old data")
            if self.user_backups:
                resource_to_patch = self._patches
                self._backups = self.user_backups

            else:
                for resource, update in self._patches.items():
                    namespace = None
                    # prepare backup
                    try:
                        original_resource_dict = resource.instance.to_dict()
                    except NotFoundError:
                        # Some resource cannot be found by name.
                        # happens in 'ServiceMonitor' resource.
                        original_resource_dict = list(
                            resource.get(
                                dyn_client=resource.client,
                                field_selector=f"metadata.name={resource.name}",
                            )
                        )[0].to_dict()
                        namespace = update.get("metadata", {}).get("namespace")

                    backup = self._create_backup(
                        original=original_resource_dict, patch=update
                    )
                    if namespace:
                        # Add namespace to metadata for restore.
                        backup["metadata"]["namespace"] = namespace

                    # no need to back up if no changes have been made
                    # if action is 'replace' we need to update even if no backup (replace update can be empty )
                    if backup or self.action == "replace":
                        resource_to_patch.append(resource)
                        self._backups[resource] = backup
                    else:
                        LOGGER.warning(
                            f"ResourceEdit: no diff found in patch for "
                            f"{resource.name} -- skipping"
                        )
                if not resource_to_patch:
                    return
        else:
            resource_to_patch = self._patches

        patches_to_apply = {
            resource: self._patches[resource] for resource in resource_to_patch
        }

        # apply changes
        self._apply_patches_sampler(
            patches=patches_to_apply, action_text="Updating", action=self.action
        )

    def restore(self):
        self._apply_patches_sampler(
            patches=self._backups, action_text="Restoring", action=self.action
        )

    def __enter__(self):
        self.update(backup_resources=True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # restore backups
        self.restore()

    @staticmethod
    def _dictify_resourcefield(res):
        """Recursively turns any ResourceField objects into dicts to avoid issues caused by appending lists, etc."""
        if isinstance(res, ResourceField):
            return ResourceEditor._dictify_resourcefield(res=dict(res.items()))
        elif isinstance(res, dict):
            return {
                ResourceEditor._dictify_resourcefield(
                    res=key
                ): ResourceEditor._dictify_resourcefield(res=value)
                for key, value in res.items()
            }
        elif isinstance(res, list):
            return [ResourceEditor._dictify_resourcefield(res=x) for x in res]

        return res

    @staticmethod
    def _create_backup(original, patch):
        """
        Args:
            original (dict*): source of values to back up if necessary
            patch (dict*): 'new' values; keys needn't necessarily all be
                contained in original

        Returns a dict containing the fields in original that are different
        from update. Performs the

        Places None for fields in update that don't appear in
        original (because that's how the API knows to remove those fields from
        the yaml).

        * the first call will be with both of these arguments as dicts but
        this will not necessarily be the case during recursion"""

        # when both are dicts, get the diff (recursively if need be)
        if isinstance(original, dict) and isinstance(patch, dict):
            diff_dict = {}
            for key, value in patch.items():
                if key not in original:
                    diff_dict[key] = None
                    continue

                # recursive call
                key_diff = ResourceEditor._create_backup(
                    original=original[key], patch=value
                )

                if key_diff is not None:
                    diff_dict[key] = key_diff

            return diff_dict

        # for one or more non-dict values, just compare them
        if patch != original:
            return original
        else:
            # this return value will be received by key_diff above
            return None

    @staticmethod
    def _apply_patches(patches, action_text, action):
        """
        Updates provided Resource objects with provided yaml patches

        Args:
            patches (dict): {<Resource object>: <yaml patch as dict>}
            action_text (str):
                "ResourceEdit <action_text> for resource <resource name>"
                will be printed for each resource; see below
        """

        for resource, patch in patches.items():
            LOGGER.info(
                f"ResourceEdits: {action_text} data for "
                f"resource {resource.kind} {resource.name}"
            )

            # add name to patch
            if "metadata" not in patch:
                patch["metadata"] = {}

            # the api requires this field to be present in a yaml patch for
            # some resource kinds even if it is not changed
            if "name" not in patch["metadata"]:
                patch["metadata"]["name"] = resource.name

            if action == "update":
                resource.update(resource_dict=patch)  # update the resource

            if action == "replace":
                if "metadata" not in patch:
                    patch["metadata"] = {}

                patch["metadata"]["name"] = resource.name
                patch["metadata"]["namespace"] = resource.namespace
                patch["metadata"][
                    "resourceVersion"
                ] = resource.instance.metadata.resourceVersion
                patch["kind"] = resource.kind
                patch["apiVersion"] = resource.api_version

                resource.update_replace(
                    resource_dict=patch
                )  # replace the resource metadata

    def _apply_patches_sampler(self, patches, action_text, action):
        exceptions_dict = {ConflictError: []}
        exceptions_dict.update(DEFAULT_CLUSTER_RETRY_EXCEPTIONS)
        return Resource.retry_cluster_exceptions(
            func=self._apply_patches,
            exceptions_dict=exceptions_dict,
            patches=patches,
            action_text=action_text,
            action=action,
        )
