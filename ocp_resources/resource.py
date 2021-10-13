import contextlib
import json
import logging
import os
import re
from distutils.version import Version

import kubernetes
import urllib3
import yaml
from openshift.dynamic import DynamicClient
from openshift.dynamic.exceptions import (
    ConflictError,
    InternalServerError,
    NotFoundError,
    ServerTimeoutError,
)
from openshift.dynamic.resource import ResourceField

from ocp_resources.constants import (
    NOT_FOUND_ERROR_EXCEPTION_DICT,
    PROTOCOL_ERROR_EXCEPTION_DICT,
)
from ocp_resources.utils import TimeoutExpiredError, TimeoutSampler


DEFAULT_CLUSTER_RETRY_EXCEPTIONS = {
    ConnectionAbortedError: [],
    ConnectionResetError: [],
    InternalServerError: ["etcdserver: leader changed"],
    ServerTimeoutError: [],
}

LOGGER = logging.getLogger(__name__)
TIMEOUT = 240
MAX_SUPPORTED_API_VERSION = "v1"


def _collect_instance_data(directory, resource_object):
    with open(os.path.join(directory, f"{resource_object.name}.yaml"), "w") as fd:
        fd.write(resource_object.instance.to_str())


def _collect_pod_logs(dyn_client, resource_item, **kwargs):
    kube_v1_api = kubernetes.client.CoreV1Api(api_client=dyn_client.client)
    return kube_v1_api.read_namespaced_pod_log(
        name=resource_item.metadata.name,
        namespace=resource_item.metadata.namespace,
        **kwargs,
    )


def _collect_virt_launcher_data(dyn_client, directory, resource_object):
    if resource_object.kind == "VirtualMachineInstance":
        for pod in dyn_client.resources.get(kind="Pod").get().items:
            pod_name = pod.metadata.name
            pod_instance = dyn_client.resources.get(
                api_version=pod.apiVersion, kind=pod.kind
            ).get(name=pod_name, namespace=pod.metadata.namespace)
            if pod_name.startswith("virt-launcher"):
                with open(os.path.join(directory, f"{pod_name}.log"), "w") as fd:
                    fd.write(
                        _collect_pod_logs(
                            dyn_client=dyn_client,
                            resource_item=pod,
                            container="compute",
                        )
                    )

                with open(os.path.join(directory, f"{pod_name}.yaml"), "w") as fd:
                    fd.write(pod_instance.to_str())


def _collect_data_volume_data(dyn_client, directory, resource_object):
    if resource_object.kind == "DataVolume":
        cdi_worker_prefixes = ("importer", "cdi-upload")
        for pod in dyn_client.resources.get(kind="Pod").get().items:
            pod_name = pod.metadata.name
            pod_instance = dyn_client.resources.get(
                api_version=pod.apiVersion, kind=pod.kind
            ).get(name=pod_name, namespace=pod.metadata.namespace)
            if pod_name.startswith(cdi_worker_prefixes) or pod_name.endswith(
                "source-pod"
            ):
                with open(os.path.join(directory, f"{pod_name}.log"), "w") as fd:
                    fd.write(
                        _collect_pod_logs(dyn_client=dyn_client, resource_item=pod)
                    )

                with open(os.path.join(directory, f"{pod_name}.yaml"), "w") as fd:
                    fd.write(pod_instance.to_str())


def _collect_data(resource_object, dyn_client=None):
    dyn_client = (
        dyn_client
        if dyn_client
        else DynamicClient(kubernetes.config.new_client_from_config())
    )
    directory = os.environ.get("TEST_DIR_LOG")
    _collect_instance_data(directory=directory, resource_object=resource_object)
    _collect_virt_launcher_data(
        dyn_client=dyn_client, directory=directory, resource_object=resource_object
    )
    _collect_data_volume_data(
        dyn_client=dyn_client, directory=directory, resource_object=resource_object
    )


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
    return res.group_version


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
        super().__init__(vstring=vstring)

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

    class Status:
        SUCCEEDED = "Succeeded"
        FAILED = "Failed"
        DELETING = "Deleting"
        DEPLOYED = "Deployed"
        PENDING = "Pending"
        COMPLETED = "Completed"
        RUNNING = "Running"
        TERMINATING = "Terminating"

    class Condition:
        UPGRADEABLE = "Upgradeable"
        AVAILABLE = "Available"
        DEGRADED = "Degraded"
        PROGRESSING = "Progressing"
        CREATED = "Created"
        RECONCILE_COMPLETE = "ReconcileComplete"
        READY = "Ready"

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
        CDI_KUBEVIRT_IO = "cdi.kubevirt.io"
        CONFIG_OPENSHIFT_IO = "config.openshift.io"
        CONSOLE_OPENSHIFT_IO = "console.openshift.io"
        EVENTS_K8S_IO = "events.k8s.io"
        FORKLIFT_KONVEYOR_IO = "forklift.konveyor.io"
        HCO_KUBEVIRT_IO = "hco.kubevirt.io"
        HOSTPATHPROVISIONER_KUBEVIRT_IO = "hostpathprovisioner.kubevirt.io"
        IMAGE_OPENSHIFT_IO = "image.openshift.io"
        K8S_CNI_CNCF_IO = "k8s.cni.cncf.io"
        K8S_V1_CNI_CNCF_IO = "k8s.v1.cni.cncf.io"
        KUBERNETES_IO = "kubernetes.io"
        KUBEVIRT_IO = "kubevirt.io"
        KUBEVIRT_KUBEVIRT_IO = "kubevirt.kubevirt.io"
        LITMUS_IO = "litmuschaos.io"
        MACHINE_OPENSHIFT_IO = "machine.openshift.io"
        MACHINECONFIGURATION_OPENSHIFT_IO = "machineconfiguration.openshift.io"
        MAISTRA_IO = "maistra.io"
        MONITORING_COREOS_COM = "monitoring.coreos.com"
        NETWORKADDONSOPERATOR_NETWORK_KUBEVIRT_IO = (
            "networkaddonsoperator.network.kubevirt.io"
        )
        NETWORKING_ISTIO_IO = "networking.istio.io"
        NETWORKING_K8S_IO = "networking.k8s.io"
        NMSTATE_IO = "nmstate.io"
        NODEMAINTENANCE_KUBEVIRT_IO = "nodemaintenance.kubevirt.io"
        OPERATOR_OPENSHIFT_IO = "operator.openshift.io"
        OPERATORS_COREOS_COM = "operators.coreos.com"
        OPERATORS_OPENSHIFT_IO = "operators.openshift.io"
        OS_TEMPLATE_KUBEVIRT_IO = "os.template.kubevirt.io"
        PACKAGES_OPERATORS_COREOS_COM = "packages.operators.coreos.com"
        POLICY = "policy"
        PROJECT_OPENSHIFT_IO = "project.openshift.io"
        RBAC_AUTHORIZATION_K8S_IO = "rbac.authorization.k8s.io"
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
        TEMPLATE_KUBEVIRT_IO = "template.kubevirt.io"
        TEMPLATE_OPENSHIFT_IO = "template.openshift.io"
        UPLOAD_CDI_KUBEVIRT_IO = "upload.cdi.kubevirt.io"
        V2V_KUBEVIRT_IO = "v2v.kubevirt.io"
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
        timeout=TIMEOUT,
        privileged_client=None,
        yaml_file=None,
    ):
        """
        Create a API resource

        Args:
            name (str): Resource name
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
        if not (self.name or self.yaml_file):
            raise ValueError("name or yaml file is required")

        if not self.client:
            try:
                self.client = DynamicClient(
                    client=kubernetes.config.new_client_from_config()
                )
            except (
                kubernetes.config.ConfigException,
                urllib3.exceptions.MaxRetryError,
            ):
                LOGGER.error(
                    "You need to be logged into a cluster or have $KUBECONFIG env configured"
                )
                raise
        if not self.api_version:
            self.api_version = _get_api_version(
                dyn_client=self.client, api_group=self.api_group, kind=self.kind
            )

        self.teardown = teardown
        self.timeout = timeout

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
            with open(self.yaml_file, "r") as stream:
                self.resource_dict = yaml.safe_load(stream=stream.read())
                self.name = self.resource_dict["metadata"]["name"]
                return self.resource_dict

        return {
            "apiVersion": self.api_version,
            "kind": self.kind,
            "metadata": {"name": self.name},
        }

    def to_dict(self):
        """
        Generate intended dict representation of the resource.
        """
        return self._base_body()

    def __enter__(self):
        return self.deploy()

    def __exit__(self, exception_type, exception_value, traceback):
        if self.teardown:
            self.clean_up()

    def deploy(self):
        self.create()
        return self

    def clean_up(self):
        if os.environ.get("CNV_TEST_COLLECT_LOGS", "0") == "1":
            try:
                _collect_data(resource_object=self)
            except Exception as exception_:
                LOGGER.warning(exception_)

        data = self.to_dict()
        LOGGER.info(f"Deleting {data}")
        self.delete(wait=True, timeout=self.timeout)

    @classmethod
    def _prepare_resources(cls, dyn_client, singular_name, *args, **kwargs):
        if not cls.api_version:
            cls.api_version = _get_api_version(
                dyn_client=dyn_client, api_group=cls.api_group, kind=cls.kind
            )

        get_kwargs = {"singular_name": singular_name} if singular_name else {}
        return dyn_client.resources.get(
            kind=cls.kind, api_version=cls.api_version, **get_kwargs
        ).get(*args, **kwargs)

    def _prepare_singular_name_kwargs(self, **kwargs):
        kwargs = kwargs if kwargs else {}
        if self.singular_name:
            kwargs["singular_name"] = self.singular_name

        return kwargs

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
        kwargs = self._prepare_singular_name_kwargs(**kwargs)

        return self.client.resources.get(
            api_version=self.api_version, kind=self.kind, **kwargs
        )

    @property
    def api(self):
        return self.full_api()

    def wait(self, timeout=TIMEOUT, sleep=1):
        """
        Wait for resource

        Args:
            timeout (int): Time to wait for the resource.
            sleep (int): Time to wait between retries

        Raises:
            TimeoutExpiredError: If resource not exists.
        """
        LOGGER.info(f"Wait until {self.kind} {self.name} is created")
        samples = TimeoutSampler(
            wait_timeout=timeout,
            sleep=sleep,
            exceptions_dict={
                **PROTOCOL_ERROR_EXCEPTION_DICT,
                **NOT_FOUND_ERROR_EXCEPTION_DICT,
            },
            func=lambda: self.exists,
        )
        for sample in samples:
            if sample:
                return

    def wait_deleted(self, timeout=TIMEOUT):
        """
        Wait until resource is deleted

        Args:
            timeout (int): Time to wait for the resource.

        Raises:
            TimeoutExpiredError: If resource still exists.
        """
        LOGGER.info(f"Wait until {self.kind} {self.name} is deleted")
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

    def wait_for_status(self, status, timeout=TIMEOUT, stop_status=None, sleep=1):
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
        LOGGER.info(f"Wait for {self.kind} {self.name} status to be {status}")
        samples = TimeoutSampler(
            wait_timeout=timeout,
            sleep=sleep,
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
                        current_status = sample_status.phase
                        if current_status == status:
                            return

                        if current_status == stop_status:
                            raise TimeoutExpiredError(
                                f"Status of {self.kind} {self.name} is {current_status}"
                            )

        except TimeoutExpiredError:
            if current_status:
                LOGGER.error(f"Status of {self.kind} {self.name} is {current_status}")
            raise

    def create(self, body=None, wait=False):
        """
        Create resource.

        Args:
            body (dict): Resource data to create.
            wait (bool) : True to wait for resource status.

        Returns:
            bool: True if create succeeded, False otherwise.

        Raises:
            ValueMismatch: When body value doesn't match class value
        """
        data = self.to_dict()
        if body:
            kind = body["kind"]
            name = body.get("name")
            api_version = body["apiVersion"]
            if kind != self.kind:
                raise ValueMismatch(f"{kind} != {self.kind}")
            if name and name != self.name:
                raise ValueMismatch(f"{name} != {self.name}")
            if api_version != self.api_version:
                raise ValueMismatch(f"{api_version} != {self.api_version}")

            data.update(body)

        LOGGER.info(f"Posting {data}")
        LOGGER.info(f"Create {self.kind} {self.name}")
        res = self.api.create(body=data, namespace=self.namespace)
        if wait and res:
            return self.wait()
        return res

    def delete(self, wait=False, timeout=TIMEOUT, body=None):
        try:
            res = self.api.delete(name=self.name, namespace=self.namespace, body=body)
        except NotFoundError:
            return False

        LOGGER.info(f"Delete {self.kind} {self.name}")
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
        LOGGER.info(f"Get {self.kind} {self.name} status")
        return self.instance.status.phase

    def update(self, resource_dict):
        """
        Update resource with resource dict

        Args:
            resource_dict: Resource dictionary
        """
        LOGGER.info(f"Update {self.kind} {self.name}: {resource_dict}")
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
        LOGGER.info(f"Replace {self.kind} {self.name}: {resource_dict}")
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
    def get(cls, dyn_client, singular_name=None, *args, **kwargs):
        """
        Get resources

        Args:
            dyn_client (DynamicClient): Open connection to remote cluster
            singular_name (str): Resource kind (in lowercase), in use where we have multiple matches for resource

        Returns:
            generator: Generator of Resources of cls.kind
        """

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

    def wait_for_condition(self, condition, status, timeout=300):
        """
        Wait for Pod condition to be in desire status.

        Args:
            condition (str): Condition to query.
            status (str): Expected condition status.
            timeout (int): Time to wait for the resource.

        Raises:
            TimeoutExpiredError: If Pod condition in not in desire status.
        """
        LOGGER.info(
            f"Wait for {self.kind}/{self.name}'s '{condition}' condition to be '{status}'"
        )
        samples = TimeoutSampler(
            wait_timeout=timeout,
            sleep=1,
            exceptions_dict=PROTOCOL_ERROR_EXCEPTION_DICT,
            func=self.api.get,
            field_selector=f"metadata.name=={self.name}",
            namespace=self.namespace,
        )
        for sample in samples:
            if (
                sample.items
                and sample.items[0].get("status")
                and sample.items[0].status.get("conditions")
            ):
                sample_conditions = sample.items[0].status.conditions
                if sample_conditions:
                    for cond in sample_conditions:
                        if cond.type == condition and cond.status == status:
                            return

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
        timeout=TIMEOUT,
        privileged_client=None,
        yaml_file=None,
    ):
        super().__init__(
            name=name,
            client=client,
            teardown=teardown,
            timeout=timeout,
            privileged_client=privileged_client,
            yaml_file=yaml_file,
        )
        self.namespace = namespace
        if not (self.name and self.namespace) and not self.yaml_file:
            raise ValueError("name and namespace or yaml file is required")

    @classmethod
    def get(cls, dyn_client, singular_name=None, raw=False, *args, **kwargs):
        """
        Get resources

        Args:
            dyn_client (DynamicClient): Open connection to remote cluster
            singular_name (str): Resource kind (in lowercase), in use where we have multiple matches for resource
            raw (bool): If True return raw object from openshift-restclient-python


        Returns:
            generator: Generator of Resources of cls.kind
        """
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
        res = super(NamespacedResource, self)._base_body()
        if self.yaml_file:
            self.namespace = self.resource_dict["metadata"].get(
                "namespace", self.namespace
            )

        if not self.namespace:
            raise ValueError("Namespace must be passed or specified in the YAML file.")

        if not self.yaml_file:
            res["metadata"]["namespace"] = self.namespace

        return res

    def to_dict(self):
        return self._base_body()


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
