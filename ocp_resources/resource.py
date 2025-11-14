import base64
import contextlib
import copy
import json
import os
import re
import sys
import threading
from abc import ABC, abstractmethod
from collections.abc import Callable, Generator
from io import StringIO
from signal import SIGINT, signal
from types import TracebackType
from typing import Any, Self
from urllib.parse import parse_qs, urlencode, urlparse

import jsonschema
import kubernetes
import requests
import yaml
from benedict import benedict
from kubernetes.dynamic import DynamicClient, ResourceInstance
from kubernetes.dynamic.exceptions import (
    ConflictError,
    ForbiddenError,
    MethodNotAllowedError,
    NotFoundError,
    ResourceNotFoundError,
)
from kubernetes.dynamic.resource import ResourceField
from packaging.version import Version
from simple_logger.logger import get_logger, logging
from timeout_sampler import (
    TimeoutExpiredError,
    TimeoutSampler,
    TimeoutWatch,
)
from urllib3.exceptions import MaxRetryError

from fake_kubernetes_client.dynamic_client import FakeDynamicClient
from ocp_resources.event import Event
from ocp_resources.exceptions import (
    ClientWithBasicAuthError,
    MissingRequiredArgumentError,
    MissingResourceResError,
    ResourceTeardownError,
    ValidationError,
)
from ocp_resources.utils.constants import (
    DEFAULT_CLUSTER_RETRY_EXCEPTIONS,
    NOT_FOUND_ERROR_EXCEPTION_DICT,
    PROTOCOL_ERROR_EXCEPTION_DICT,
    TIMEOUT_1MINUTE,
    TIMEOUT_1SEC,
    TIMEOUT_4MINUTES,
    TIMEOUT_5SEC,
    TIMEOUT_10SEC,
    TIMEOUT_30SEC,
)
from ocp_resources.utils.resource_constants import ResourceConstants
from ocp_resources.utils.schema_validator import SchemaValidator
from ocp_resources.utils.utils import skip_existing_resource_creation_teardown

LOGGER = get_logger(name=__name__)
MAX_SUPPORTED_API_VERSION = "v2"


def _find_supported_resource(dyn_client: DynamicClient, api_group: str, kind: str) -> ResourceField | None:
    results = dyn_client.resources.search(group=api_group, kind=kind)
    sorted_results = sorted(results, key=lambda result: KubeAPIVersion(result.api_version), reverse=True)
    for result in sorted_results:
        if KubeAPIVersion(result.api_version) <= KubeAPIVersion(MAX_SUPPORTED_API_VERSION):
            return result
    return None


def _get_api_version(dyn_client: DynamicClient, api_group: str, kind: str) -> str:
    # Returns api_group/api_version
    res = _find_supported_resource(dyn_client=dyn_client, api_group=api_group, kind=kind)
    log = f"Couldn't find {kind} in {api_group} api group"

    if not res:
        LOGGER.warning(log)
        raise NotImplementedError(log)

    if isinstance(res.group_version, str):
        LOGGER.info(f"kind: {kind} api version: {res.group_version}")
        return res.group_version

    raise NotImplementedError(log)


def client_configuration_with_basic_auth(
    username: str,
    password: str,
    host: str,
    configuration: kubernetes.client.Configuration,
) -> kubernetes.client.ApiClient:
    verify_ssl = configuration.verify_ssl

    def _fetch_oauth_config(_host: str, _verify_ssl: bool) -> Any:
        well_known_url = f"{_host}/.well-known/oauth-authorization-server"

        config_response = requests.get(well_known_url, verify=_verify_ssl)
        if config_response.status_code != 200:
            raise ClientWithBasicAuthError("No well-known file found at endpoint")

        return config_response.json()

    def _get_authorization_code(_auth_endpoint: str, _username: str, _password: str, _verify_ssl: bool) -> str:
        _code = None
        auth_params = {
            "client_id": "openshift-challenging-client",
            "response_type": "code",
            "state": "USER",
            "code_challenge_method": "S256",
        }

        auth_url = f"{_auth_endpoint}?{urlencode(auth_params)}"

        credentials = f"{_username}:{_password}"
        auth_header = base64.b64encode(credentials.encode()).decode()

        auth_response = requests.get(
            auth_url,
            headers={"Authorization": f"Basic {auth_header}", "X-CSRF-Token": "USER", "Accept": "application/json"},
            verify=_verify_ssl,
            allow_redirects=False,
        )

        if auth_response.status_code == 302:
            location = auth_response.headers.get("Location", "")

            parsed_url = urlparse(location)
            query_params = parse_qs(parsed_url.query)
            _code = query_params.get("code", [None])[0]
        if _code:
            return _code

        raise ClientWithBasicAuthError("No authorization code found")

    def _exchange_code_for_token(
        _token_endpoint: str, _auth_code: str, _verify_ssl: bool
    ) -> kubernetes.client.ApiClient:
        _client = None

        token_data = {
            "grant_type": "authorization_code",
            "code": _auth_code,
            "client_id": "openshift-challenging-client",
        }

        token_response = requests.post(
            _token_endpoint,
            data=token_data,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
                # openshift-challenging-client:
                "Authorization": "Basic b3BlbnNoaWZ0LWNoYWxsZW5naW5nLWNsaWVudDo=",
            },
            verify=_verify_ssl,
        )

        if token_response.status_code == 200:
            token_json = token_response.json()
            access_token = token_json.get("access_token")

            configuration.host = host
            configuration.api_key = {"authorization": f"Bearer {access_token}"}
            _client = kubernetes.client.ApiClient(configuration=configuration)

        if _client:
            return _client

        raise ClientWithBasicAuthError("Failed to authenticate with basic auth")

    oauth_config = _fetch_oauth_config(_host=host, _verify_ssl=verify_ssl)

    auth_endpoint = oauth_config.get("authorization_endpoint")
    if not auth_endpoint:
        raise ClientWithBasicAuthError("No authorization_endpoint found in well-known file")

    _code = _get_authorization_code(
        _auth_endpoint=auth_endpoint, _username=username, _password=password, _verify_ssl=verify_ssl
    )

    return _exchange_code_for_token(
        _token_endpoint=oauth_config.get("token_endpoint"), _auth_code=_code, _verify_ssl=verify_ssl
    )


def get_client(
    config_file: str | None = None,
    config_dict: dict[str, Any] | None = None,
    context: str | None = None,
    client_configuration: kubernetes.client.Configuration | None = None,
    persist_config: bool = True,
    temp_file_path: str | None = None,
    try_refresh_token: bool = True,
    username: str | None = None,
    password: str | None = None,
    host: str | None = None,
    verify_ssl: bool | None = None,
    token: str | None = None,
    fake: bool = False,
) -> DynamicClient | FakeDynamicClient:
    """
    Get a kubernetes client.


    This function is a replica of `ocp_utilities.infra.get_client` which cannot be imported as ocp_utilities imports
    from ocp_resources.

    Pass either config_file or config_dict.
    If none of them are passed, client will be created from default OS kubeconfig
    (environment variable or .kube folder).

    Args:
        config_file (str): path to a kubeconfig file.
        config_dict (dict): dict with kubeconfig configuration.
        context (str): name of the context to use.
        persist_config (bool): whether to persist config file.
        temp_file_path (str): path to a temporary kubeconfig file.
        try_refresh_token (bool): try to refresh token
        username (str): username for basic auth
        password (str): password for basic auth
        host (str): host for the cluster
        verify_ssl (bool): whether to verify ssl
        token (str): Use token to login

    Returns:
        DynamicClient: a kubernetes client.
    """
    if fake:
        return FakeDynamicClient()

    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("HTTP_PROXY")

    client_configuration = client_configuration or kubernetes.client.Configuration()

    if verify_ssl is not None:
        client_configuration.verify_ssl = verify_ssl

    if not client_configuration.proxy and proxy:
        LOGGER.info(f"Setting proxy from environment variable: {proxy}")
        client_configuration.proxy = proxy

    if username and password and host:
        _client = client_configuration_with_basic_auth(
            username=username, password=password, host=host, configuration=client_configuration
        )

    elif host and token:
        client_configuration.host = host
        client_configuration.api_key = {"authorization": f"Bearer {token}"}
        _client = kubernetes.client.ApiClient(client_configuration)

    # Ref: https://github.com/kubernetes-client/python/blob/v26.1.0/kubernetes/base/config/kube_config.py
    elif config_dict:
        _client = kubernetes.config.new_client_from_config_dict(
            config_dict=config_dict,
            context=context,
            client_configuration=client_configuration,
            persist_config=persist_config,
            temp_file_path=temp_file_path,
        )
    else:
        # Ref: https://github.com/kubernetes-client/python/blob/v26.1.0/kubernetes/base/config/__init__.py
        LOGGER.info("Trying to get client via new_client_from_config")

        # kubernetes.config.kube_config.load_kube_config sets KUBE_CONFIG_DEFAULT_LOCATION during module import.
        # If `KUBECONFIG` environment variable is set via code, the `KUBE_CONFIG_DEFAULT_LOCATION` will be None since
        # is populated during import which comes before setting the variable in code.
        config_file = config_file or os.environ.get("KUBECONFIG", "~/.kube/config")

        _client = kubernetes.config.new_client_from_config(
            config_file=config_file,
            context=context,
            client_configuration=client_configuration,
            persist_config=persist_config,
        )

    kubernetes.client.Configuration.set_default(default=client_configuration)

    try:
        return kubernetes.dynamic.DynamicClient(client=_client)
    except MaxRetryError:
        # Ref: https://github.com/kubernetes-client/python/blob/v26.1.0/kubernetes/base/config/incluster_config.py
        LOGGER.info("Trying to get client via incluster_config")
        return kubernetes.dynamic.DynamicClient(
            client=kubernetes.config.incluster_config.load_incluster_config(
                client_configuration=client_configuration, try_refresh_token=try_refresh_token
            ),
        )


def sub_resource_level(current_class: Any, owner_class: Any, parent_class: Any) -> str | None:
    # return the name of the last class in MRO list that is not one of base
    # classes; otherwise return None
    for class_iterator in reversed([
        class_iterator
        for class_iterator in current_class.mro()
        if class_iterator not in owner_class.mro() and issubclass(class_iterator, parent_class)
    ]):
        return class_iterator.__name__

    return None


def replace_key_with_hashed_value(resource_dict: dict[Any, Any], key_name: str) -> dict[Any, Any]:
    """
    Recursively search a nested dictionary for a given key and changes its value to "******" if found.

    The function supports two key formats:
    1. Regular dictionary path:
        A key to be hashed can be found directly in a dictionary, e.g. "a>b>c", would hash the value associated with
        key "c", where dictionary format is:
        input = {
            "a": {
                "b": {
                    "c": "sensitive data"
                }
            }
        }
        output = {
            "a": {
                "b": {
                    "c": "*******"
                }
            }
        }
    2. list path:
        A key to be hashed can be found in a dictionary that is in list somewhere in a dictionary, e.g. "a>b[]>c",
        would hash the value associated with key "c", where dictionary format is:
        input = {
            "a": {
                "b": [
                    {"d": "not sensitive data"},
                    {"c": "sensitive data"}
                ]
            }
        }
        output = {
            "a": {
                "b": [
                    {"d": "not sensitive data"},
                    {"c": "*******"}
                ]
            }
        }

    Args:
        resource_dict: The nested dictionary to search.
        key_name: The key path to find.

    Returns:
        dict[Any, Any]: A copy of the input dictionary with the specified key's value replaced with "*******".

    """
    result = copy.deepcopy(resource_dict)

    benedict_resource_dict = benedict(result, keypath_separator=">")

    if "[]" not in key_name:
        if benedict_resource_dict.get(key_name):
            benedict_resource_dict[key_name] = "*******"
        return dict(benedict_resource_dict)

    key_prefix, remaining_key = key_name.split("[]>", 1)
    if not benedict_resource_dict.get(key_prefix):
        return dict(benedict_resource_dict)

    resource_data = benedict_resource_dict[key_prefix]
    if not isinstance(resource_data, list):
        return dict(benedict_resource_dict)

    for index, element in enumerate(resource_data):
        if isinstance(element, dict):
            resource_data[index] = replace_key_with_hashed_value(resource_dict=element, key_name=remaining_key)

    return dict(benedict_resource_dict)


class KubeAPIVersion(Version):
    """
    Implement the Kubernetes API versioning scheme from
    https://kubernetes.io/docs/concepts/overview/kubernetes-api/#api-versioning
    """

    component_re = re.compile(r"(\d+ | [a-z]+)", re.VERBOSE)

    def __init__(self, vstring: str):
        self.vstring = vstring
        self.version: list[str | Any] = []
        super().__init__(version=vstring)

    def parse(self, vstring: str) -> None:
        components = [comp for comp in self.component_re.split(vstring) if comp]
        for idx, obj in enumerate(components):
            with contextlib.suppress(ValueError):
                components[idx] = int(obj)

        errmsg = f"version '{vstring}' does not conform to kubernetes api versioning guidelines"

        if len(components) not in (2, 4) or components[0] != "v" or not isinstance(components[1], int):
            raise ValueError(errmsg)

        if len(components) == 4 and (components[2] not in ("alpha", "beta") or not isinstance(components[3], int)):
            raise ValueError(errmsg)

        self.version = components

    def __str__(self):
        return self.vstring

    def __repr__(self):
        return f"KubeAPIVersion ('{str(self)}')"

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
    def __init__(self, func: Callable) -> None:
        self.func = func

    def __get__(self, obj: Any, owner: Any) -> Any:
        return self.func(owner)


class Resource(ResourceConstants):
    """
    Base class for API resources

    Provides common functionality for all Kubernetes/OpenShift resources including
    CRUD operations, resource management, and schema validation.

    Attributes:
        api_group (str): API group for the resource (e.g., "apps", "batch")
        api_version (str): API version (e.g., "v1", "v1beta1")
        singular_name (str): Singular resource name for API calls
        timeout_seconds (int): Default timeout for API operations
        schema_validation_enabled (bool): Enable automatic validation on create/update
    """

    api_group: str = ""
    api_version: str = ""
    singular_name: str = ""
    timeout_seconds: int = TIMEOUT_1MINUTE

    class ApiGroup:
        AAQ_KUBEVIRT_IO: str = "aaq.kubevirt.io"
        ADMISSIONREGISTRATION_K8S_IO: str = "admissionregistration.k8s.io"
        APIEXTENSIONS_K8S_IO: str = "apiextensions.k8s.io"
        APIREGISTRATION_K8S_IO: str = "apiregistration.k8s.io"
        APP_KUBERNETES_IO: str = "app.kubernetes.io"
        APPS: str = "apps"
        APPSTUDIO_REDHAT_COM: str = "appstudio.redhat.com"
        AUTHENTICATION_K8S_IO: str = "authentication.k8s.io"
        BATCH: str = "batch"
        BITNAMI_COM: str = "bitnami.com"
        CACHING_INTERNAL_KNATIVE_DEV: str = "caching.internal.knative.dev"
        CDI_KUBEVIRT_IO: str = "cdi.kubevirt.io"
        CLONE_KUBEVIRT_IO: str = "clone.kubevirt.io"
        CLUSTER_OPEN_CLUSTER_MANAGEMENT_IO: str = "cluster.open-cluster-management.io"
        COMPONENTS_PLATFORM_OPENDATAHUB_IO = "components.platform.opendatahub.io"
        CONFIG_OPENSHIFT_IO: str = "config.openshift.io"
        CONSOLE_OPENSHIFT_IO: str = "console.openshift.io"
        COORDINATION_K8S_IO: str = "coordination.k8s.io"
        CSIADDONS_OPENSHIFT_IO: str = "csiaddons.openshift.io"
        DATA_IMPORT_CRON_TEMPLATE_KUBEVIRT_IO: str = "dataimportcrontemplate.kubevirt.io"
        DATASCIENCECLUSTER_OPENDATAHUB_IO: str = "datasciencecluster.opendatahub.io"
        DATASCIENCEPIPELINESAPPLICATIONS_OPENDATAHUB_IO: str = "datasciencepipelinesapplications.opendatahub.io"
        DISCOVERY_K8S_IO: str = "discovery.k8s.io"
        DSCINITIALIZATION_OPENDATAHUB_IO: str = "dscinitialization.opendatahub.io"
        EVENTS_K8S_IO: str = "events.k8s.io"
        EXPORT_KUBEVIRT_IO: str = "export.kubevirt.io"
        FENCE_AGENTS_REMEDIATION_MEDIK8S_IO: str = "fence-agents-remediation.medik8s.io"
        FORKLIFT_KONVEYOR_IO: str = "forklift.konveyor.io"
        FRRK8S_METALLB_IO = "frrk8s.metallb.io"
        GATEWAY_NETWORKING_K8S_IO: str = "gateway.networking.k8s.io"
        HCO_KUBEVIRT_IO: str = "hco.kubevirt.io"
        HELM_MARIADB_MMONTES_IO: str = "helm.mariadb.mmontes.io"
        HIVE_OPENSHIFT_IO: str = "hive.openshift.io"
        HOSTPATHPROVISIONER_KUBEVIRT_IO: str = "hostpathprovisioner.kubevirt.io"
        IMAGE_OPENSHIFT_IO: str = "image.openshift.io"
        IMAGE_REGISTRY: str = "registry.redhat.io"
        IMAGEREGISTRY_OPERATOR_OPENSHIFT_IO: str = "imageregistry.operator.openshift.io"
        INSTANCETYPE_KUBEVIRT_IO: str = "instancetype.kubevirt.io"
        INTEGREATLY_ORG: str = "integreatly.org"
        JAEGERTRACING_IO = "jaegertracing.io"
        K8S_CNI_CNCF_IO: str = "k8s.cni.cncf.io"
        K8S_MARIADB_COM: str = "k8s.mariadb.com"
        K8S_OVN_ORG: str = "k8s.ovn.org"
        K8S_V1_CNI_CNCF_IO: str = "k8s.v1.cni.cncf.io"
        KEDA_SH: str = "keda.sh"
        KUBEFLOW_ORG: str = "kubeflow.org"
        KUBERNETES_IO: str = "kubernetes.io"
        KUBEVIRT_IO: str = "kubevirt.io"
        KUBEVIRT_KUBEVIRT_IO: str = "kubevirt.kubevirt.io"
        LITMUS_IO: str = "litmuschaos.io"
        LLAMASTACK_IO: str = "llamastack.io"
        MACHINE_OPENSHIFT_IO: str = "machine.openshift.io"
        MACHINECONFIGURATION_OPENSHIFT_IO: str = "machineconfiguration.openshift.io"
        MAISTRA_IO: str = "maistra.io"
        METALLB_IO: str = "metallb.io"
        METRICS_K8S_IO: str = "metrics.k8s.io"
        MIGRATION_OPENSHIFT_IO: str = "migration.openshift.io"
        MIGRATIONS_KUBEVIRT_IO: str = "migrations.kubevirt.io"
        MODELREGISTRY_OPENDATAHUB_IO: str = "modelregistry.opendatahub.io"
        MONITORING_COREOS_COM: str = "monitoring.coreos.com"
        MTQ_KUBEVIRT_IO: str = "mtq.kubevirt.io"
        NETWORKADDONSOPERATOR_NETWORK_KUBEVIRT_IO: str = "networkaddonsoperator.network.kubevirt.io"
        NETWORKING_ISTIO_IO: str = "networking.istio.io"
        NETWORKING_K8S_IO: str = "networking.k8s.io"
        NMSTATE_IO: str = "nmstate.io"
        NODE_LABELLER_KUBEVIRT_IO: str = "node-labeller.kubevirt.io"
        NODEMAINTENANCE_KUBEVIRT_IO: str = "nodemaintenance.kubevirt.io"
        OBSERVABILITY_OPEN_CLUSTER_MANAGEMENT_IO: str = "observability.open-cluster-management.io"
        OCS_OPENSHIFT_IO: str = "ocs.openshift.io"
        OPENTELEMETRY_IO: str = "opentelemetry.io"
        OPERATOR_AUTHORINO_KUADRANT_IO: str = "operator.authorino.kuadrant.io"
        OPERATOR_OPEN_CLUSTER_MANAGEMENT_IO: str = "operator.open-cluster-management.io"
        OPERATOR_OPENSHIFT_IO: str = "operator.openshift.io"
        OPERATORS_COREOS_COM: str = "operators.coreos.com"
        OPERATORS_OPENSHIFT_IO: str = "operators.openshift.io"
        OS_TEMPLATE_KUBEVIRT_IO: str = "os.template.kubevirt.io"
        PACKAGES_OPERATORS_COREOS_COM: str = "packages.operators.coreos.com"
        PERFORMANCE_OPENSHIFT_IO: str = "performance.openshift.io"
        POLICY: str = "policy"
        POOL_KUBEVIRT_IO: str = "pool.kubevirt.io"
        PROJECT_OPENSHIFT_IO: str = "project.openshift.io"
        QUOTA_OPENSHIFT_IO: str = "quota.openshift.io"
        RBAC_AUTHORIZATION_K8S_IO: str = "rbac.authorization.k8s.io"
        REMEDIATION_MEDIK8S_IO: str = "remediation.medik8s.io"
        RIPSAW_CLOUDBULLDOZER_IO: str = "ripsaw.cloudbulldozer.io"
        ROUTE_OPENSHIFT_IO: str = "route.openshift.io"
        SAMPLES_OPERATOR_OPENSHIFT_IO: str = "samples.operator.openshift.io"
        SCHEDULING_K8S_IO: str = "scheduling.k8s.io"
        SECURITY_ISTIO_IO: str = "security.istio.io"
        SECURITY_OPENSHIFT_IO: str = "security.openshift.io"
        SELF_NODE_REMEDIATION_MEDIK8S_IO: str = "self-node-remediation.medik8s.io"
        SERVICES_PLATFORM_OPENDATAHUB_IO: str = "services.platform.opendatahub.io"
        SERVING_KNATIVE_DEV: str = "serving.knative.dev"
        SERVING_KSERVE_IO: str = "serving.kserve.io"
        SNAPSHOT_KUBEVIRT_IO: str = "snapshot.kubevirt.io"
        SNAPSHOT_STORAGE_K8S_IO: str = "snapshot.storage.k8s.io"
        SRIOVNETWORK_OPENSHIFT_IO: str = "sriovnetwork.openshift.io"
        SSP_KUBEVIRT_IO: str = "ssp.kubevirt.io"
        STORAGE_K8S_IO: str = "storage.k8s.io"
        STORAGECLASS_KUBERNETES_IO: str = "storageclass.kubernetes.io"
        STORAGECLASS_KUBEVIRT_IO: str = "storageclass.kubevirt.io"
        SUBRESOURCES_KUBEVIRT_IO: str = "subresources.kubevirt.io"
        TEKTON_DEV: str = "tekton.dev"
        TEKTONTASKS_KUBEVIRT_IO: str = "tektontasks.kubevirt.io"
        TEMPLATE_KUBEVIRT_IO: str = "template.kubevirt.io"
        TEMPLATE_OPENSHIFT_IO: str = "template.openshift.io"
        TEMPO_GRAFANA_COM: str = "tempo.grafana.com"
        TRUSTYAI_OPENDATAHUB_IO: str = "trustyai.opendatahub.io"
        UPLOAD_CDI_KUBEVIRT_IO: str = "upload.cdi.kubevirt.io"
        USER_OPENSHIFT_IO: str = "user.openshift.io"
        V2V_KUBEVIRT_IO: str = "v2v.kubevirt.io"
        VELERO_IO: str = "velero.io"
        VM_KUBEVIRT_IO: str = "vm.kubevirt.io"

    class ApiVersion:
        V1: str = "v1"
        V1BETA1: str = "v1beta1"
        V1ALPHA1: str = "v1alpha1"
        V1ALPHA3: str = "v1alpha3"

    def __init__(
        self,
        name: str | None = None,
        client: DynamicClient | None = None,
        teardown: bool = True,
        yaml_file: str | None = None,
        delete_timeout: int = TIMEOUT_4MINUTES,
        dry_run: bool = False,
        node_selector: dict[str, Any] | None = None,
        node_selector_labels: dict[str, str] | None = None,
        config_file: str | None = None,
        config_dict: dict[str, Any] | None = None,
        context: str | None = None,
        label: dict[str, str] | None = None,
        annotations: dict[str, str] | None = None,
        api_group: str = "",
        hash_log_data: bool = True,
        ensure_exists: bool = False,
        kind_dict: dict[Any, Any] | None = None,
        wait_for_resource: bool = False,
        schema_validation_enabled: bool = False,
    ):
        """
        Create an API resource

        If `yaml_file` or `kind_dict` are passed, logic in `to_dict` is bypassed.

        Args:
            name (str): Resource name
            client (DynamicClient): Dynamic client for connecting to a remote cluster
            teardown (bool): Indicates if this resource would need to be deleted
            yaml_file (str): yaml file for the resource
            delete_timeout (int): timeout associated with delete action
            dry_run (bool): dry run
            node_selector (dict): node selector
            node_selector_labels (str): node selector labels
            config_file (str): Path to config file for connecting to remote cluster.
            context (str): Context name for connecting to remote cluster.
            label (dict): Resource labels
            annotations (dict[str, str] | None): Resource annotations
            api_group (str): Resource API group; will overwrite API group definition in resource class
            hash_log_data (bool): Hash resource content based on resource keys_to_hash property
                (example: Secret resource)
            ensure_exists (bool): Whether to check if the resource exists before when initializing the resource, raise if not.
            kind_dict (dict): dict which represents the resource object
            wait_for_resource (bool): Waits for the resource to be created
            schema_validation_enabled (bool): Enable automatic schema validation for this instance.
                Defaults to False. Set to True to validate on create/update operations.
        """
        if yaml_file and kind_dict:
            raise ValueError("yaml_file and resource_dict are mutually exclusive")

        self.name = name
        self.teardown = teardown
        self.yaml_file = yaml_file
        self.kind_dict = kind_dict
        self.delete_timeout = delete_timeout
        self.dry_run = dry_run
        self.node_selector = node_selector
        self.node_selector_labels = node_selector_labels
        self.config_file = config_file
        self.config_dict = config_dict or {}
        self.context = context
        self.label = label
        self.annotations = annotations
        self.client: DynamicClient = client or get_client(config_file=self.config_file, context=self.context)
        self.api_group: str = api_group or self.api_group
        self.hash_log_data = hash_log_data

        if not self.api_group and not self.api_version:
            raise NotImplementedError("Subclasses of Resource require self.api_group or self.api_version to be defined")

        if not (self.name or self.yaml_file or self.kind_dict):
            raise MissingRequiredArgumentError(argument="name")

        self.namespace: str | None = None
        self.node_selector_spec = self._prepare_node_selector_spec()
        self.res: dict[Any, Any] = self.kind_dict or {}
        self.yaml_file_contents: str = ""
        self.initial_resource_version: str = ""
        self.logger = self._set_logger()
        self.wait_for_resource = wait_for_resource

        if ensure_exists:
            self._ensure_exists()

        # Set instance-level validation flag
        self.schema_validation_enabled = schema_validation_enabled

        # self._set_client_and_api_version() must be last init line
        self._set_client_and_api_version()

    def _ensure_exists(self) -> None:
        if not self.exists:
            _name_for_raise = self.name if not self.namespace else f"{self.namespace}/{self.name}"
            raise ResourceNotFoundError(f"Resource `{self.kind}` `{_name_for_raise}` does not exist")

    def _set_logger(self) -> logging.Logger:
        log_level = os.environ.get("OPENSHIFT_PYTHON_WRAPPER_LOG_LEVEL", "INFO")
        log_file = os.environ.get("OPENSHIFT_PYTHON_WRAPPER_LOG_FILE", "")
        return get_logger(
            name=f"{__name__.rsplit('.')[0]} {self.kind}",
            level=log_level,
            filename=log_file,
        )

    def _prepare_node_selector_spec(self) -> dict[str, str]:
        return self.node_selector or self.node_selector_labels or {}

    @ClassProperty
    def kind(cls) -> str | None:
        return sub_resource_level(cls, NamespacedResource, Resource)

    def _base_body(self) -> None:
        """
        Generate resource dict from yaml if self.yaml_file else return base resource dict.

        Returns:
            dict: Resource dict.
        """
        if self.kind_dict:
            # If `kind_dict` is provided, no additional logic should be applied
            self.name = self.kind_dict["metadata"]["name"]

        elif self.yaml_file:
            if not self.yaml_file_contents:
                if isinstance(self.yaml_file, StringIO):
                    self.yaml_file_contents = self.yaml_file.read()

                else:
                    with open(self.yaml_file) as stream:
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

            if self.label:
                self.res.setdefault("metadata", {}).setdefault("labels", {}).update(self.label)

            if self.annotations:
                self.res.setdefault("metadata", {}).setdefault("annotations", {}).update(self.annotations)

        if not self.res:
            raise MissingResourceResError(name=self.name or "")

    def to_dict(self) -> None:
        """
        Generate intended dict representation of the resource.
        """
        self._base_body()

    def __enter__(self) -> Any:
        if threading.current_thread().native_id == threading.main_thread().native_id:
            signal(SIGINT, self._sigint_handler)
        return self.deploy(wait=self.wait_for_resource)

    def __exit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_val: BaseException | None = None,
        exc_tb: TracebackType | None = None,
    ) -> None:
        if self.teardown:
            if not self.clean_up():
                raise ResourceTeardownError(resource=self)

    def _sigint_handler(self, signal_received: int, _frame: Any) -> None:
        self.__exit__()
        sys.exit(signal_received)

    def deploy(self, wait: bool = False) -> Self:
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

    def clean_up(self, wait: bool = True, timeout: int | None = None) -> bool:
        """
        For debug, export SKIP_RESOURCE_TEARDOWN to skip resource teardown.
        Spaces are important in the export dict

        Args:
            wait (bool, optional): Wait for resource deletion. Defaults to True.
            timeout (int, optional): Timeout in seconds to wait for resource to be deleted. Defaults to 240.

        Returns:
            bool: True if resource was deleted else False.

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
            return True

        return self.delete(wait=wait, timeout=timeout or self.delete_timeout)

    @classmethod
    def _prepare_resources(
        cls, dyn_client: DynamicClient, singular_name: str, *args: Any, **kwargs: Any
    ) -> ResourceInstance:
        if not cls.api_version:
            cls.api_version = _get_api_version(dyn_client=dyn_client, api_group=cls.api_group, kind=cls.kind)

        get_kwargs = {"singular_name": singular_name} if singular_name else {}
        return dyn_client.resources.get(
            kind=cls.kind,
            api_version=cls.api_version,
            **get_kwargs,
        ).get(*args, **kwargs, timeout_seconds=cls.timeout_seconds)

    def _prepare_singular_name_kwargs(self, **kwargs: Any) -> dict[str, Any]:
        kwargs = kwargs if kwargs else {}
        if self.singular_name:
            kwargs["singular_name"] = self.singular_name

        return kwargs

    def _set_client_and_api_version(self) -> None:
        if not self.client:
            self.client = get_client(config_file=self.config_file, context=self.context)

        if not self.api_version:
            self.api_version = _get_api_version(dyn_client=self.client, api_group=self.api_group, kind=self.kind)

    def full_api(self, **kwargs: Any) -> ResourceInstance:
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

        return self.client.resources.get(api_version=self.api_version, kind=self.kind, **kwargs)

    @property
    def api(self) -> ResourceInstance:
        return self.full_api()

    def wait(self, timeout: int = TIMEOUT_4MINUTES, sleep: int = 1) -> None:
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

    def wait_deleted(self, timeout: int = TIMEOUT_4MINUTES) -> bool:
        """
        Wait until resource is deleted

        Args:
            timeout (int): Time to wait for the resource.

        Raises:
            TimeoutExpiredError: If resource still exists.
        """
        self.logger.info(f"Wait until {self.kind} {self.name} is deleted")
        try:
            for sample in TimeoutSampler(wait_timeout=timeout, sleep=1, func=lambda: self.exists):
                if not sample:
                    return True
        except TimeoutExpiredError:
            self.logger.warning(f"Timeout expired while waiting for {self.kind} {self.name} to be deleted")
            return False

        return False

    @property
    def exists(self) -> ResourceInstance | None:
        """
        Whether self exists on the server
        """
        try:
            return self.instance
        except NotFoundError:
            return None

    @property
    def _kube_v1_api(self) -> kubernetes.client.CoreV1Api:
        return kubernetes.client.CoreV1Api(api_client=self.client.client)

    def wait_for_status(
        self, status: str, timeout: int = TIMEOUT_4MINUTES, stop_status: str | None = None, sleep: int = 1
    ) -> None:
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
            func=lambda: self.exists,
        )
        current_status = None
        last_logged_status = None
        try:
            for sample in samples:
                if sample:
                    instance_dict = sample.to_dict()
                    current_status = instance_dict.get("status", {}).get("phase")

                    if current_status != last_logged_status:
                        last_logged_status = current_status
                        self.logger.info(f"Status of {self.kind} {self.name} is {current_status}")

                    if current_status == status:
                        return

                    if current_status == stop_status:
                        raise TimeoutExpiredError(f"Status of {self.kind} {self.name} is {current_status}")

        except TimeoutExpiredError:
            if current_status:
                self.logger.error(f"Status of {self.kind} {self.name} is {current_status}")
            raise

    def create(
        self, wait: bool = False, exceptions_dict: dict[type[Exception], list[str]] = DEFAULT_CLUSTER_RETRY_EXCEPTIONS
    ) -> ResourceInstance | None:
        """
        Create resource.

        Args:
            wait (bool) : True to wait for resource status.
            exceptions_dict (dict[type[Exception], list[str]]): Dictionary of exceptions to retry on.

        Returns:
            ResourceInstance | None: Created resource instance or None if create failed.
        """
        self.to_dict()

        # Validate the resource if auto-validation is enabled
        if self.schema_validation_enabled:
            self.validate()

        hashed_res = self.hash_resource_dict(resource_dict=self.res)
        self.logger.info(f"Create {self.kind} {self.name}")
        self.logger.info(f"Posting {hashed_res}")
        self.logger.debug(f"\n{yaml.dump(hashed_res)}")
        resource_kwargs: dict[str, Any] = {"body": self.res, "namespace": self.namespace}
        if self.dry_run:
            resource_kwargs["dry_run"] = "All"

        resource_ = Resource.retry_cluster_exceptions(
            func=self.api.create, exceptions_dict=exceptions_dict, **resource_kwargs
        )
        with contextlib.suppress(ForbiddenError, AttributeError, NotFoundError):
            # some resources do not support get() (no instance) or the client do not have permissions
            self.initial_resource_version = self.instance.metadata.resourceVersion

        if wait and resource_:
            self.wait()
        return resource_

    def delete(self, wait: bool = False, timeout: int = TIMEOUT_4MINUTES, body: dict[str, Any] | None = None) -> bool:
        self.logger.info(f"Delete {self.kind} {self.name}")

        if self.exists:
            _instance_dict = self.instance.to_dict()
            if isinstance(_instance_dict, dict):
                hashed_data = self.hash_resource_dict(resource_dict=_instance_dict)
                self.logger.info(f"Deleting {hashed_data}")
                self.logger.debug(f"\n{yaml.dump(hashed_data)}")

            else:
                self.logger.warning(f"{self.kind}: {self.name} instance.to_dict() return was not a dict")

            self.api.delete(name=self.name, namespace=self.namespace, body=body)

            if wait:
                return self.wait_deleted(timeout=timeout)

            return True

        self.logger.warning(f"Resource {self.kind} {self.name} was not found, and wasn't deleted")
        return True

    @property
    def status(self) -> str:
        """
        Get resource status

        Status: Running, Scheduling, Pending, Unknown, CrashLoopBackOff

        Returns:
           str: Status
        """
        self.logger.info(f"Get {self.kind} {self.name} status")
        return self.instance.status.phase

    def update(self, resource_dict: dict[str, Any]) -> None:
        """
        Update resource with resource dict

        Args:
            resource_dict: Resource dictionary
        """
        # Note: We don't validate on update() because this method sends a patch,
        # not a complete resource. Patches are partial updates that would fail
        # full schema validation.

        hashed_resource_dict = self.hash_resource_dict(resource_dict=resource_dict)
        self.logger.info(f"Update {self.kind} {self.name}:\n{hashed_resource_dict}")
        self.logger.debug(f"\n{yaml.dump(hashed_resource_dict)}")
        self.api.patch(
            body=resource_dict,
            namespace=self.namespace,
            content_type="application/merge-patch+json",
        )

    def update_replace(self, resource_dict: dict[str, Any]) -> None:
        """
        Replace resource metadata.
        Use this to remove existing field. (update() will only update existing fields)
        """
        # Validate the resource if auto-validation is enabled
        # For replace operations, we validate the full resource_dict
        if self.schema_validation_enabled:
            # Use validate_dict to validate the replacement resource
            self.__class__.validate_dict(resource_dict)

        hashed_resource_dict = self.hash_resource_dict(resource_dict=resource_dict)
        self.logger.info(f"Replace {self.kind} {self.name}: \n{hashed_resource_dict}")
        self.logger.debug(f"\n{yaml.dump(hashed_resource_dict)}")
        self.api.replace(body=resource_dict, name=self.name, namespace=self.namespace)

    @staticmethod
    def retry_cluster_exceptions(
        func: Callable,
        exceptions_dict: dict[type[Exception], list[str]] = DEFAULT_CLUSTER_RETRY_EXCEPTIONS,
        timeout: int = TIMEOUT_10SEC,
        sleep_time: int = 1,
        **kwargs: Any,
    ) -> Any:
        try:
            sampler = TimeoutSampler(
                wait_timeout=timeout,
                sleep=sleep_time,
                func=func,
                print_log=False,
                exceptions_dict=exceptions_dict,
                **kwargs,
            )
            for sample in sampler:
                return sample

        except TimeoutExpiredError as exp:
            if exp.last_exp:
                raise exp.last_exp from exp

            raise

    @classmethod
    def get(
        cls,
        config_file: str = "",
        singular_name: str = "",
        exceptions_dict: dict[type[Exception], list[str]] = DEFAULT_CLUSTER_RETRY_EXCEPTIONS,
        raw: bool = False,
        context: str | None = None,
        dyn_client: DynamicClient | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> Generator[Any, None, None]:
        """
        Get resources

        Args:
            dyn_client (DynamicClient): Open connection to remote cluster.
            config_file (str): Path to config file for connecting to remote cluster.
            context (str): Context name for connecting to remote cluster.
            singular_name (str): Resource kind (in lowercase), in use where we have multiple matches for resource.
            raw (bool): If True return raw object.
            exceptions_dict (dict): Exceptions dict for TimeoutSampler

        Returns:
            generator: Generator of Resources of cls.kind.
        """
        if not dyn_client:
            dyn_client = get_client(config_file=config_file, context=context)

        def _get() -> Generator["Resource|ResourceInstance", None, None]:
            _resources = cls._prepare_resources(*args, dyn_client=dyn_client, singular_name=singular_name, **kwargs)  # type: ignore[misc]
            try:
                for resource_field in _resources.items:
                    if raw:
                        yield _resources
                    else:
                        yield cls(client=dyn_client, name=resource_field.metadata.name)

            except TypeError:
                if raw:
                    yield _resources
                else:
                    yield cls(client=dyn_client, name=_resources.metadata.name)

        return Resource.retry_cluster_exceptions(func=_get, exceptions_dict=exceptions_dict)

    @property
    def instance(self) -> ResourceInstance:
        """
        Get resource instance

        Returns:
            openshift.dynamic.client.ResourceInstance
        """

        def _instance() -> ResourceInstance | None:
            return self.api.get(name=self.name)

        return self.retry_cluster_exceptions(func=_instance)

    @property
    def labels(self) -> ResourceField:
        """
        Method to get labels for this resource

        Returns:
           openshift.dynamic.resource.ResourceField: Representation of labels
        """
        return self.instance.get("metadata", {})["labels"]

    def watcher(self, timeout: int, resource_version: str = "") -> Generator[dict[str, Any], None, None]:
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

    def wait_for_condition(
        self,
        condition: str,
        status: str,
        timeout: int = 300,
        sleep_time: int = 1,
        reason: str | None = None,
        message: str = "",
    ) -> None:
        """
        Wait for Resource condition to be in desire status.

        Args:
            condition (str): Condition to query.
            status (str): Expected condition status.
            reason (None): Expected condition reason.
            message (str): Expected condition text inclusion.
            timeout (int): Time to wait for the resource.
            sleep_time(int): Interval between each retry when checking the resource's condition.

        Raises:
            TimeoutExpiredError: If Resource condition in not in desire status.
        """
        self.logger.info(f"Wait for {self.kind}/{self.name}'s '{condition}' condition to be '{status}'")

        timeout_watcher = TimeoutWatch(timeout=timeout)
        self.wait(timeout=timeout, sleep=sleep_time)
        for sample in TimeoutSampler(
            wait_timeout=timeout_watcher.remaining_time(),
            sleep=sleep_time,
            func=lambda: self.instance,
        ):
            if sample:
                for cond in sample.get("status", {}).get("conditions", []):
                    actual_condition = {"type": cond["type"], "status": cond["status"]}
                    expected_condition = {"type": condition, "status": status}
                    if reason is not None:
                        actual_condition["reason"] = cond.get("reason", "")
                        expected_condition["reason"] = reason

                    if actual_condition == expected_condition and message in cond.get("message", ""):
                        return

    def api_request(
        self, method: str, action: str, url: str, retry_params: dict[str, int] | None = None, **params: Any
    ) -> dict[str, Any]:
        """
        Handle API requests to resource.

        Args:
            method (str): Request method (GET/PUT etc.).
            action (str): Action to perform (stop/start/guestosinfo etc.).
            url (str): URL of resource.
            retry_params (dict): dict of timeout and sleep_time values for retrying the api request call

        Returns:
           data(dict): response data

        """
        client: DynamicClient = self.client
        api_request_params = {
            "url": f"{url}/{action}",
            "method": method,
            "headers": client.client.configuration.api_key,
        }
        if retry_params:
            response = self.retry_cluster_exceptions(
                func=client.client.request,
                timeout=retry_params.get("timeout", TIMEOUT_10SEC),
                sleep_time=retry_params.get("sleep_time", TIMEOUT_1SEC),
                **api_request_params,
                **params,
            )
        else:
            response = client.client.request(
                **api_request_params,
                **params,
            )
        try:
            return json.loads(response.data)
        except json.decoder.JSONDecodeError:
            return response.data

    def wait_for_conditions(self) -> None:
        timeout_watcher = TimeoutWatch(timeout=30)
        for sample in TimeoutSampler(
            wait_timeout=TIMEOUT_30SEC,
            sleep=1,
            func=lambda: self.exists,
        ):
            if sample:
                break

        samples = TimeoutSampler(
            wait_timeout=timeout_watcher.remaining_time(),
            sleep=1,
            func=lambda: self.instance.status.conditions,
        )
        for sample in samples:
            if sample:
                return

    def events(
        self,
        name: str = "",
        label_selector: str = "",
        field_selector: str = "",
        resource_version: str = "",
        timeout: int = TIMEOUT_4MINUTES,
    ) -> Generator[Any, Any, None]:
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
        client: DynamicClient | None = None,
        config_file: str = "",
        context: str | None = None,
        config_dict: dict[str, Any] | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> Generator[ResourceField, None, None]:
        """
        Get all cluster resources

        Args:
            client (DynamicClient): k8s client
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
        if not client:
            client = get_client(config_file=config_file, config_dict=config_dict, context=context)

        for _resource in client.resources.search():
            try:
                _resources = client.get(_resource, *args, **kwargs)
                yield from _resources.items

            except (NotFoundError, TypeError, MethodNotAllowedError):
                continue

    def to_yaml(self) -> str:
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

    @property
    def keys_to_hash(self) -> list[str]:
        """
        Resource attributes list to hash in the logs.

        The list should hold absolute key paths in resource dict.

         Example:
             given a dict: {"spec": {"data": <value_to_hash>}}
             To hash spec['data'] key pass: ["spec>data"]
        """
        return []

    def hash_resource_dict(self, resource_dict: dict[Any, Any]) -> dict[Any, Any]:
        if not isinstance(resource_dict, dict):
            raise ValueError("Expected a dictionary as the first argument")

        if os.environ.get("OPENSHIFT_PYTHON_WRAPPER_HASH_LOG_DATA", "true") == "false":
            return resource_dict

        if self.keys_to_hash and self.hash_log_data:
            resource_dict = copy.deepcopy(resource_dict)
            for key_name in self.keys_to_hash:
                resource_dict = replace_key_with_hashed_value(resource_dict=resource_dict, key_name=key_name)

        return resource_dict

    def get_condition_message(self, condition_type: str, condition_status: str = "") -> str:
        """
        Get condition message by condition type and condition status

        Args:
            condition_type (str): condition type name
            condition_status (str, optional): condition status to match

        Returns:
            str: condition message or empty string if condition status doesn't match
        """
        if _conditions := self.instance.status.conditions:
            for condition in _conditions:
                if condition_type == condition.type:
                    if not condition_status:
                        return condition.message

                    if condition_status == condition.status:
                        return condition.message

                    self.logger.error(
                        f"Condition `{condition_type}` status is not `{condition_status}`, got `{condition.status}`"
                    )
                    break

        return ""

    def validate(self) -> None:
        """
        Validate the resource against its OpenAPI schema.

        This method validates the resource dictionary (self.res) against the
        appropriate OpenAPI schema for this resource type. If validation fails,
        a ValidationError is raised with details about what is invalid.

        Note: This method is called automatically during create() and update()
        operations if schema_validation_enabled was set to True when creating
        the resource instance.

        Raises:
            ValidationError: If the resource is invalid according to the schema
        """

        # Get resource dict - if self.res is already populated, use it directly
        # Otherwise, try to build it with to_dict()
        if not self.res:
            try:
                self.to_dict()  # This populates self.res
            except Exception:
                # If to_dict fails (e.g., missing required fields),
                # we can't validate - let the original error propagate
                raise

        resource_dict = self.res

        # Validate using shared validator
        try:
            SchemaValidator.validate(resource_dict=resource_dict, kind=self.kind, api_group=self.api_group)
        except jsonschema.ValidationError as e:
            error_msg = SchemaValidator.format_validation_error(
                error=e, kind=self.kind, name=self.name or "unnamed", api_group=self.api_group
            )
            raise ValidationError(error_msg) from e
        except Exception as e:
            LOGGER.error(f"Unexpected error during validation: {e}")
            raise

    @classmethod
    def validate_dict(cls, resource_dict: dict[str, Any]) -> None:
        """
        Validate a resource dictionary against the schema.

        Args:
            resource_dict: Dictionary representation of the resource

        Raises:
            ValidationError: If the resource dict is invalid
        """

        # Get name for error messages
        name = resource_dict.get("metadata", {}).get("name", "unnamed")

        # Validate using shared validator
        try:
            SchemaValidator.validate(resource_dict=resource_dict, kind=cls.kind, api_group=cls.api_group)
        except jsonschema.ValidationError as e:
            error_msg = SchemaValidator.format_validation_error(
                error=e, kind=cls.kind, name=name, api_group=cls.api_group
            )
            raise ValidationError(error_msg) from e
        except Exception as e:
            LOGGER.error(f"Unexpected error during validation: {e}")
            raise


class NamespacedResource(Resource):
    """
    Namespaced object, inherited from Resource.
    """

    def __init__(
        self,
        name: str | None = None,
        namespace: str | None = None,
        teardown: bool = True,
        yaml_file: str | None = None,
        delete_timeout: int = TIMEOUT_4MINUTES,
        client: DynamicClient | None = None,
        ensure_exists: bool = False,
        **kwargs: Any,
    ):
        super().__init__(
            name=name,
            client=client,
            teardown=teardown,
            yaml_file=yaml_file,
            delete_timeout=delete_timeout,
            **kwargs,
        )
        self.namespace = namespace
        if not (self.name and self.namespace) and not self.yaml_file and not self.kind_dict:
            raise MissingRequiredArgumentError(argument="'name' and 'namespace'")

        if ensure_exists:
            self._ensure_exists()

    @classmethod
    def get(
        cls,
        config_file: str = "",
        singular_name: str = "",
        exceptions_dict: dict[type[Exception], list[str]] = DEFAULT_CLUSTER_RETRY_EXCEPTIONS,
        raw: bool = False,
        context: str | None = None,
        dyn_client: DynamicClient | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> Generator[Any, None, None]:
        """
        Get resources

        Args:
            dyn_client (DynamicClient): Open connection to remote cluster
            config_file (str): Path to config file for connecting to remote cluster.
            context (str): Context name for connecting to remote cluster.
            singular_name (str): Resource kind (in lowercase), in use where we have multiple matches for resource.
            raw (bool): If True return raw object.
            exceptions_dict (dict): Exceptions dict for TimeoutSampler

        Returns:
            generator: Generator of Resources of cls.kind
        """
        if not dyn_client:
            dyn_client = get_client(config_file=config_file, context=context)

        def _get() -> Generator["NamespacedResource|ResourceInstance", None, None]:
            _resources = cls._prepare_resources(*args, dyn_client=dyn_client, singular_name=singular_name, **kwargs)  # type: ignore[misc]
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

        return Resource.retry_cluster_exceptions(func=_get, exceptions_dict=exceptions_dict)

    @property
    def instance(self) -> ResourceInstance:
        """
        Get resource instance

        Returns:
            openshift.dynamic.client.ResourceInstance
        """

        def _instance() -> ResourceInstance:
            return self.api.get(name=self.name, namespace=self.namespace)

        return self.retry_cluster_exceptions(func=_instance)

    def _base_body(self) -> None:
        if self.yaml_file or self.kind_dict:
            self.namespace = self.res["metadata"].get("namespace", self.namespace)

        else:
            self.res["metadata"]["namespace"] = self.namespace

        if not self.namespace:
            raise MissingRequiredArgumentError(argument="namespace")

    def to_dict(self) -> None:
        super()._base_body()
        self._base_body()


class ResourceEditor:
    def __init__(
        self, patches: dict[Any, Any], action: str = "update", user_backups: dict[Any, Any] | None = None
    ) -> None:
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
        self._backups: dict[Any, Any] = {}

    @property
    def backups(self) -> dict[Any, Any]:
        """Returns a dict {<Resource object>: <backup_as_dict>}
        The backup dict kept for each resource edited"""
        return self._backups

    @property
    def patches(self) -> dict[Any, Any]:
        """Returns the patches dict provided in the constructor"""
        return self._patches

    def update(self, backup_resources: bool = False) -> None:
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

                    backup = self._create_backup(original=original_resource_dict, patch=update)
                    if namespace:
                        # Add namespace to metadata for restore.
                        backup["metadata"]["namespace"] = namespace

                    # no need to back up if no changes have been made
                    # if action is 'replace' we need to update even if no backup (replace update can be empty )
                    if backup or self.action == "replace":
                        resource_to_patch.append(resource)
                        self._backups[resource] = backup
                    else:
                        LOGGER.warning(f"ResourceEdit: no diff found in patch for {resource.name} -- skipping")
                if not resource_to_patch:
                    return
        else:
            resource_to_patch = self._patches

        patches_to_apply = {resource: self._patches[resource] for resource in resource_to_patch}

        # apply changes
        self._apply_patches_sampler(patches=patches_to_apply, action_text="Updating", action=self.action)

    def restore(self) -> None:
        self._apply_patches_sampler(patches=self._backups, action_text="Restoring", action=self.action)

    def __enter__(self) -> Self:
        self.update(backup_resources=True)
        return self

    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None:
        # restore backups
        self.restore()

    @staticmethod
    def _dictify_resourcefield(res: Any) -> Any:
        """Recursively turns any ResourceField objects into dicts to avoid issues caused by appending lists, etc."""
        if isinstance(res, ResourceField):
            return ResourceEditor._dictify_resourcefield(res=dict(res.items()))

        elif isinstance(res, dict):
            return {
                ResourceEditor._dictify_resourcefield(res=key): ResourceEditor._dictify_resourcefield(res=value)
                for key, value in res.items()
            }

        elif isinstance(res, list):
            return [ResourceEditor._dictify_resourcefield(res=x) for x in res]

        return res

    @staticmethod
    def _create_backup(original: dict[Any, Any], patch: dict[Any, Any]) -> dict[Any, Any]:
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
            diff_dict: dict[Any, Any] = {}
            for key, value in patch.items():
                if key not in original:
                    diff_dict[key] = None
                    continue

                # recursive call
                key_diff = ResourceEditor._create_backup(original=original[key], patch=value)

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
    def _apply_patches(patches: dict[Any, Any], action_text: str, action: str) -> None:
        """
        Updates provided Resource objects with provided yaml patches

        Args:
            patches (dict): {<Resource object>: <yaml patch as dict>}
            action_text (str):
                "ResourceEdit <action_text> for resource <resource name>"
                will be printed for each resource; see below
        """

        for resource, patch in patches.items():
            LOGGER.info(f"ResourceEdits: {action_text} data for resource {resource.kind} {resource.name}")

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
                patch["metadata"]["resourceVersion"] = resource.instance.metadata.resourceVersion
                patch["kind"] = resource.kind
                patch["apiVersion"] = resource.api_version

                # replace the resource metadata
                resource.update_replace(resource_dict=patch)

    def _apply_patches_sampler(self, patches: dict[Any, Any], action_text: str, action: str) -> ResourceInstance:
        exceptions_dict: dict[type[Exception], list[str]] = {ConflictError: []}
        exceptions_dict.update(DEFAULT_CLUSTER_RETRY_EXCEPTIONS)
        return Resource.retry_cluster_exceptions(
            func=self._apply_patches,
            exceptions_dict=exceptions_dict,
            patches=patches,
            action_text=action_text,
            action=action,
            timeout=TIMEOUT_30SEC,
            sleep_time=TIMEOUT_5SEC,
        )


class BaseResourceList(ABC):
    """
    Abstract base class for managing collections of resources.

    Provides common functionality for resource lists including context management,
    iteration, indexing, deployment, and cleanup operations.
    """

    def __init__(self, client: DynamicClient) -> None:
        self.resources: list[Resource] = []
        self.client = client

    def __enter__(self) -> Self:
        """Enters the runtime context and deploys all resources."""
        self.deploy()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exits the runtime context and cleans up all resources."""
        self.clean_up()

    def __iter__(self) -> Generator[Resource | NamespacedResource, None, None]:
        """Allows iteration over the resources in the list."""
        yield from self.resources

    def __getitem__(self, index: int) -> Resource | NamespacedResource:
        """Retrieves a resource from the list by its index."""
        return self.resources[index]

    def __len__(self) -> int:
        """Returns the number of resources in the list."""
        return len(self.resources)

    def deploy(self, wait: bool = False) -> list[Resource | NamespacedResource]:
        """
        Deploys all resources in the list.

        Args:
            wait (bool): If True, wait for each resource to be ready.

        Returns:
            List[Any]: A list of the results from each resource's deploy() call.
        """
        return [resource.deploy(wait=wait) for resource in self.resources]

    def clean_up(self, wait: bool = True) -> bool:
        """
        Deletes all resources in the list.

        Args:
            wait (bool): If True, wait for each resource to be deleted.

        Returns:
            bool: Returns True if all resources are cleaned up correclty.
        """
        # Deleting in reverse order to resolve dependencies correctly.
        return all(resource.clean_up(wait=wait) for resource in reversed(self.resources))

    @abstractmethod
    def _create_resources(self, resource_class: type, **kwargs: Any) -> None:
        """Abstract method to create resources based on specific logic."""
        pass


class ResourceList(BaseResourceList):
    """
    A class to manage a collection of a specific resource type.

    This class creates and manages N copies of a given resource,
    each with a unique name derived from a base name.
    """

    def __init__(
        self,
        resource_class: type[Resource],
        num_resources: int,
        client: DynamicClient,
        **kwargs: Any,
    ) -> None:
        """
        Initializes a list of N resource objects.

        Args:
            resource_class (Type[Resource]): The resource class to instantiate (e.g., Namespace).
            num_resources (int): The number of resource copies to create.
            client (DynamicClient): The dynamic client to use. Defaults to None.
            **kwargs (Any): Arguments to be passed to the constructor of the resource_class.
                              A 'name' key is required in kwargs to serve as the base name for the resources.
        """
        super().__init__(client)

        self.num_resources = num_resources
        self._create_resources(resource_class, **kwargs)

    def _create_resources(self, resource_class: type[Resource], **kwargs: Any) -> None:
        """Creates N resources with indexed names."""
        base_name = kwargs["name"]

        for i in range(1, self.num_resources + 1):
            resource_name = f"{base_name}-{i}"
            resource_kwargs = kwargs.copy()
            resource_kwargs["name"] = resource_name

            instance = resource_class(client=self.client, **resource_kwargs)
            self.resources.append(instance)


class NamespacedResourceList(BaseResourceList):
    """
    Manages a collection of a specific namespaced resource (e.g., Pod, Service, etc), creating one instance per provided namespace.

    This class creates one copy of a given namespaced resource in each of the
    namespaces provided in a list.
    """

    def __init__(
        self,
        resource_class: type[NamespacedResource],
        namespaces: ResourceList,
        client: DynamicClient,
        **kwargs: Any,
    ) -> None:
        """
        Initializes a list of resource objects, one for each specified namespace.

        Args:
            resource_class (Type[NamespacedResource]): The namespaced resource class to instantiate (e.g., Pod).
            namespaces (ResourceList): A ResourceList containing namespaces where the resources will be created.
            client (DynamicClient): The dynamic client to use for cluster communication.
            **kwargs (Any): Additional arguments to be passed to the resource_class constructor.
                              A 'name' key is required in kwargs to serve as the base name for the resources.
        """
        for ns in namespaces:
            if ns.kind != "Namespace":
                raise TypeError("All the resources in namespaces should be namespaces.")

        super().__init__(client)

        self.namespaces = namespaces
        self._create_resources(resource_class, **kwargs)

    def _create_resources(self, resource_class: type[NamespacedResource], **kwargs: Any) -> None:
        """Creates one resource per namespace."""
        for ns in self.namespaces:
            instance = resource_class(
                namespace=ns.name,
                client=self.client,
                **kwargs,
            )
            self.resources.append(instance)
