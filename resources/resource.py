import datetime
import logging
import os
import re
import shutil
from distutils.version import Version

import kubernetes
import urllib3
from openshift.dynamic import DynamicClient
from openshift.dynamic.exceptions import NotFoundError
from resources.utils import (
    NudgeTimers,
    TimeoutExpiredError,
    TimeoutSampler,
    nudge_delete,
)
from urllib3.exceptions import ProtocolError


LOGGER = logging.getLogger(__name__)
TIMEOUT = 240
MAX_SUPPORTED_API_VERSION = "v1"


def _prepare_collect_data_directory(resource_object):
    dump_dir = "tests-collected-info"
    if not os.path.isdir(dump_dir):
        # pytest fixture create the directory, if it is not exists we probably not called from pytest.
        return

    directory = os.path.join(
        dump_dir,
        f"{'NamespaceResources/Namespaces' if resource_object.namespace else 'NotNamespaceResources'}",
        f"{resource_object.namespace if resource_object.namespace else ''}",
        resource_object.kind,
        f"{datetime.datetime.now().strftime('%H:%M:%S')}-{resource_object.name}",
    )
    if os.path.exists(directory):
        shutil.rmtree(directory, ignore_errors=True)

    os.makedirs(directory)
    return directory


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
        for pod in dyn_client.resources.get(kind="DataVolume").get().items:
            pod_name = pod.metadata.name
            pod_instance = dyn_client.resources.get(
                api_version=pod.apiVersion, kind=pod.kind
            ).get(name=pod_name, namespace=pod.metadata.namespace)
            if pod_name.startswith("cdi-importer"):
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
    directory = _prepare_collect_data_directory(resource_object=resource_object)
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
        list(
            class_iterator
            for class_iterator in current_class.mro()
            if class_iterator not in owner_class.mro()
            and issubclass(class_iterator, parent_class)
        )
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
        components = [x for x in self.component_re.split(vstring) if x]
        for i, obj in enumerate(components):
            try:
                components[i] = int(obj)
            except ValueError:
                pass

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


class classproperty(object):  # noqa: N801
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, owner):
        return self.func(owner)


class ValueMismatch(Exception):
    """
    Raises when value doesn't match the class value
    """

    pass


class Resource(object):
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

    class Condition:
        UPGRADEABLE = "Upgradeable"
        AVAILABLE = "Available"
        DEGRADED = "Degraded"
        PROGRESSING = "Progressing"
        RECONCILE_COMPLETE = "ReconcileComplete"

        class Status:
            TRUE = "True"
            FALSE = "False"

    def __init__(self, name, client=None, teardown=True):
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
            self._get_api_version()

        self.teardown = teardown

    def _get_api_version(self):
        res = _find_supported_resource(
            dyn_client=self.client, api_group=self.api_group, kind=self.kind
        )
        if not res:
            LOGGER.error(f"Couldn't find {self.kind} in {self.api_group} api group")
            raise NotImplementedError(
                f"Couldn't find {self.kind} in {self.api_group} api group"
            )
        self.api_version = _get_api_version(
            dyn_client=self.client, api_group=self.api_group, kind=self.kind
        )

    @classproperty
    def kind(cls):  # noqa: N805
        return sub_resource_level(cls, NamespacedResource, Resource)

    def _base_body(self):
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
        data = self.to_dict()
        LOGGER.info(f"Posting {data}")
        self.create_from_dict(
            dyn_client=self.client, data=data, namespace=self.namespace
        )
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if not self.teardown:
            return
        self.clean_up()

    def clean_up(self):
        if os.environ.get("CNV_TEST_COLLECT_LOGS", "0") == "1":
            try:
                _collect_data(resource_object=self)
            except Exception as exception_:
                LOGGER.warning(exception_)

        data = self.to_dict()
        LOGGER.info(f"Deleting {data}")
        self.delete(wait=True)

    def api(self, **kwargs):
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
        if self.singular_name:
            kwargs["singular_name"] = self.singular_name
        return self.client.resources.get(
            api_version=self.api_version, kind=self.kind, **kwargs
        )

    def wait(self, timeout=TIMEOUT):
        """
        Wait for resource

        Args:
            timeout (int): Time to wait for the resource.

        Raises:
            TimeoutExpiredError: If resource not exists.
        """
        LOGGER.info(f"Wait until {self.kind} {self.name} is created")
        samples = TimeoutSampler(
            timeout=timeout,
            sleep=1,
            exceptions=(ProtocolError, NotFoundError),
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
        return self._client_wait_deleted(timeout)

    def nudge_delete(self):
        """
        Resource specific "nudge delete" action that may help the resource to
        complete its cleanup. Needed by some resources.
        """

    @property
    def exists(self):
        """
        Whether self exists on the server
        """
        try:
            return self.instance
        except NotFoundError:
            return None

    def _client_wait_deleted(self, timeout):
        """
        client-side Wait until resource is deleted

        Args:
            timeout (int): Time to wait for the resource.

        Raises:
            TimeoutExpiredError: If resource still exists.
        """
        samples = TimeoutSampler(timeout=timeout, sleep=1, func=lambda: self.exists)
        for sample in samples:
            self.nudge_delete()
            if not sample:
                return

    def wait_for_status(self, status, timeout=TIMEOUT, stop_status=None):
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
            timeout=timeout,
            sleep=1,
            exceptions=ProtocolError,
            func=self.api().get,
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

    @classmethod
    def create_from_dict(cls, dyn_client, data, namespace=None):
        """
        Create resource from given yaml file.

        Args:
            dyn_client (DynamicClient): Open connection to remote cluster.
            data (dict): Dict representing the resource.
            namespace (str): Namespace of the resource unless specified in the supplied yaml.
        """
        client = dyn_client.resources.get(
            api_version=data["apiVersion"], kind=data["kind"]
        )
        LOGGER.info(f"Create {data['kind']} {data['metadata']['name']}")
        return client.create(
            body=data, namespace=data["metadata"].get("namespace", namespace)
        )

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
                ValueMismatch(f"{kind} != {self.kind}")
            if name and name != self.name:
                ValueMismatch(f"{name} != {self.name}")
            if api_version != self.api_version:
                ValueMismatch(f"{api_version} != {self.api_version}")

            data.update(body)
        res = self.api().create(body=data, namespace=self.namespace)

        LOGGER.info(f"Create {self.kind} {self.name}")
        if wait and res:
            return self.wait()
        return res

    @classmethod
    def delete_from_dict(cls, dyn_client, data, namespace=None, wait=False):
        """
        Delete resource represented by the passed data

        Args:
            dyn_client (DynamicClient): Open connection to remote cluster.
            data (dict): Dict representation of resource payload.
            namespace (str): Namespace of the resource unless specified in the supplied yaml.
            wait (bool) : True to wait for resource till deleted.

        Returns:
            True if delete succeeded, False otherwise.
        """

        def _exists(name, namespace):
            try:
                return client.get(name=name, namespace=namespace)
            except NotFoundError:
                return

        def _sampler(name, namespace, force=False):
            samples = TimeoutSampler(
                timeout=TIMEOUT, sleep=1, func=_exists, name=name, namespace=namespace
            )
            timers = NudgeTimers()
            for sample in samples:
                if force:
                    nudge_delete(name=name, timers=timers)
                if not sample:
                    return

        kind = data["kind"]
        name = data["metadata"]["name"]
        namespace = data["metadata"].get("namespace", namespace)
        client = dyn_client.resources.get(api_version=data["apiVersion"], kind=kind)
        LOGGER.info(f"Delete {data['kind']} {name}")
        res = client.delete(name=name, namespace=namespace)
        if wait and res:
            return _sampler(name, namespace, force=kind == "Namespace")
        return res

    def delete(self, wait=False):
        resource_list = self.api()
        try:
            res = resource_list.delete(name=self.name, namespace=self.namespace)
        except NotFoundError:
            return False

        LOGGER.info(f"Delete {self.kind} {self.name}")
        if wait and res:
            return self.wait_deleted()
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
        self.api().patch(
            body=resource_dict,
            namespace=self.namespace,
            content_type="application/merge-patch+json",
        )

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
        if not cls.api_version:
            cls.api_version = _get_api_version(
                dyn_client=dyn_client, api_group=cls.api_group, kind=cls.kind
            )

        get_kwargs = {"singular_name": singular_name} if singular_name else {}
        for resource_field in (
            dyn_client.resources.get(
                kind=cls.kind, api_version=cls.api_version, **get_kwargs
            )
            .get(*args, **kwargs)
            .items
        ):
            yield cls(name=resource_field.metadata.name)

    @property
    def instance(self):
        """
        Get resource instance

        Returns:
            openshift.dynamic.client.ResourceInstance
        """
        return self.api().get(name=self.name)

    @property
    def labels(self):
        """
        Method to get dict of labels for this resource

        Returns:
           labels(dict): dict labels
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
            timeout=timeout,
            sleep=1,
            exceptions=ProtocolError,
            func=self.api().get,
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


class NamespacedResource(Resource):
    """
    Namespaced object, inherited from Resource.
    """

    def __init__(self, name, namespace, client=None, teardown=True):
        super().__init__(name=name, client=client, teardown=teardown)
        self.namespace = namespace

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
        if not cls.api_version:
            cls.api_version = _get_api_version(
                dyn_client=dyn_client, api_group=cls.api_group, kind=cls.kind
            )

        get_kwargs = {"singular_name": singular_name} if singular_name else {}
        for resource_field in (
            dyn_client.resources.get(
                kind=cls.kind, api_version=cls.api_version, **get_kwargs
            )
            .get(*args, **kwargs)
            .items
        ):
            yield cls(
                name=resource_field.metadata.name,
                namespace=resource_field.metadata.namespace,
            )

    @property
    def instance(self):
        """
        Get resource instance

        Returns:
            openshift.dynamic.client.ResourceInstance
        """
        return self.api().get(name=self.name, namespace=self.namespace)


class ResourceEditor(object):
    def __init__(self, patches):
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

        self._patches = patches
        self._backups = {}

    @property
    def backups(self):
        """Returns a dict {<Resource object>: <backup_as_dict>}
        The backup dict kept for each resource edited """
        return self._backups

    @property
    def patches(self):
        """Returns the patches dict provided in the constructor"""
        return self._patches

    def update(self):
        """Prepares backup dicts (where necessary) and applies patches"""
        # prepare update dicts and backups
        LOGGER.info("ResourceEdit: Backing up old data")

        resource_to_patch = []

        for resource, update in self._patches.items():
            # prepare backup
            backup = self._create_backup(
                original=resource.instance.to_dict(), patch=update
            )

            # no need to back up if no changes have been made
            if backup:
                resource_to_patch.append(resource)
                self._backups[resource] = backup
            else:
                LOGGER.info(
                    f"ResourceEdit: no diff found in patch for "
                    f"{resource.name} -- skipping"
                )

        patches_to_apply = {
            resource: self._patches[resource] for resource in resource_to_patch
        }

        # apply changes
        self._apply_patches(patches=patches_to_apply, action_text="Updating")

    def restore(self):
        self._apply_patches(patches=self._backups, action_text="Restoring")

    def __enter__(self):
        self.update()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # restore backups
        self.restore()

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

                if key_diff:
                    diff_dict[key] = key_diff

            return diff_dict

        # for one or more non-dict values, just compare them
        if patch != original:
            return original
        else:
            # this return value will be received by key_diff above
            return None

    @staticmethod
    def _apply_patches(patches, action_text):
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

            resource.update(patch)  # update the resource
