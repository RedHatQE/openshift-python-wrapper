import os
from unittest.mock import patch

import pytest

from ocp_resources.exceptions import ResourceTeardownError
from ocp_resources.namespace import Namespace
from ocp_resources.pod import Pod
from ocp_resources.resource import NamespacedResourceList, Resource, ResourceList
from ocp_resources.secret import Secret

BASE_NAMESPACE_NAME: str = "test-namespace"
BASE_POD_NAME: str = "test-pod"
POD_CONTAINERS: list[dict[str, str]] = [{"name": "test-container", "image": "nginx:latest"}]


class SecretTestExit(Secret):
    def deploy(self, wait: bool = False):
        return self

    def clean_up(self, wait: bool = True, timeout: int | None = None) -> bool:
        return False


@pytest.fixture(scope="class")
def namespace(fake_client):
    return Namespace(client=fake_client, name=BASE_NAMESPACE_NAME)


@pytest.fixture(scope="class")
def namespaces(fake_client):
    return ResourceList(client=fake_client, resource_class=Namespace, num_resources=3, name=BASE_NAMESPACE_NAME)


@pytest.fixture(scope="class")
def pod(fake_client):
    # Create a test pod for testing purposes
    test_pod = Pod(
        client=fake_client,
        name=BASE_POD_NAME,
        namespace="default",
        containers=POD_CONTAINERS,
        annotations={"fake-client.io/ready": "false"},  # Create pod with Ready status FALSE
    )
    deployed_pod = test_pod.deploy()
    yield deployed_pod
    # Cleanup after tests
    test_pod.clean_up()


@pytest.fixture(scope="class")
def pods(fake_client, namespaces):
    return NamespacedResourceList(
        client=fake_client,
        resource_class=Pod,
        namespaces=namespaces,
        name=BASE_POD_NAME,
        containers=POD_CONTAINERS,
    )


@pytest.mark.incremental
class TestResource:
    def test_get(self, fake_client):
        for ns in Namespace.get(dyn_client=fake_client):
            assert ns.name

    def test_create(self, namespace):
        ns = namespace.deploy()
        assert ns

    def test_kind(self, namespace):
        assert namespace.kind == "Namespace"

    def test_exists(self, namespace):
        assert namespace.exists

    def test_instance(self, namespace):
        assert namespace.instance

    def test_wait_for_condition(self, pod):
        pod.wait_for_condition(condition=pod.Condition.READY, status=pod.Condition.Status.FALSE, timeout=5)

    def test_wait_for_conditions(self, pod):
        pod.wait_for_conditions()

    def test_events(self, pod):
        events = list(pod.events(timeout=1))
        assert events

    def test_get_all_cluster_resources(self, fake_client):
        for _resources in Resource.get_all_cluster_resources(client=fake_client):
            if _resources:
                break

    def test_get_condition_message(self, pod):
        assert pod.get_condition_message(
            condition_type=pod.Condition.READY, condition_status=pod.Condition.Status.FALSE
        )

    def test_wait(self, namespace):
        namespace.wait_for_status(status=Namespace.Status.ACTIVE, timeout=30)

    def test_status(self, namespace):
        assert namespace.status == Namespace.Status.ACTIVE

    def test_update(self, namespace):
        ns_dict = namespace.instance.to_dict()
        ns_dict["metadata"]["labels"].update({"test": "test"})
        namespace.update(resource_dict=ns_dict)
        assert namespace.labels["test"] == "test"

    def test_update_replace(self, namespace):
        ns_dict = namespace.instance.to_dict()
        ns_dict["metadata"]["labels"].pop("test")
        namespace.update_replace(resource_dict=ns_dict)
        assert "test" not in namespace.labels.keys()

    def test_cleanup(self, namespace):
        namespace.clean_up(wait=False)

    def test_resource_context_manager(self, fake_client):
        with Secret(name="test-context-manager", namespace="default", client=fake_client) as sec:
            pass

        assert not sec.exists

    def test_resource_context_manager_exit(self, fake_client):
        with pytest.raises(ResourceTeardownError):
            with SecretTestExit(name="test-context-manager-exit", namespace="default", client=fake_client):
                pass


@pytest.mark.incremental
class TestResourceList:
    def test_resource_list_deploy(self, namespaces):
        namespaces.deploy()
        assert namespaces

    def test_resource_list_len(self, namespaces):
        assert len(namespaces) == 3

    def test_resource_list_name(self, namespaces):
        for i, ns in enumerate(namespaces.resources, start=1):
            assert ns.name == f"{BASE_NAMESPACE_NAME}-{i}"

    def test_resource_list_teardown(self, namespaces):
        namespaces.clean_up(wait=False)

    def test_resource_list_context_manager(self, fake_client):
        with ResourceList(
            client=fake_client, resource_class=Namespace, name=BASE_NAMESPACE_NAME, num_resources=3
        ) as namespaces:
            assert namespaces


@pytest.mark.incremental
class TestNamespacedResourceList:
    def test_namespaced_resource_list_deploy(self, fake_client, pods):
        pods.deploy()
        assert pods

    def test_resource_list_len(self, namespaces, pods):
        assert len(pods) == len(namespaces)

    def test_resource_list_name(self, pods):
        for pod in pods.resources:
            assert pod.name == BASE_POD_NAME

    def test_namespaced_resource_list_namespace(self, namespaces, pods):
        for pod, namespace in zip(pods.resources, namespaces, strict=False):
            assert pod.namespace == namespace.name

    def test_resource_list_teardown(self, pods):
        pods.clean_up(wait=False)

    def test_namespaced_resource_list_context_manager(self, fake_client, namespaces):
        with NamespacedResourceList(
            client=fake_client,
            resource_class=Pod,
            namespaces=namespaces,
            name=BASE_POD_NAME,
            containers=POD_CONTAINERS,
        ) as pods:
            assert pods


@pytest.mark.xfail(reason="Need debug")
class TestClientProxy:
    @patch.dict(os.environ, {"HTTP_PROXY": "http://env-http-proxy.com"})
    def test_client_with_proxy(self, fake_client):
        http_proxy = "http://env-http-proxy.com"

        assert fake_client.configuration.proxy == http_proxy

    @patch.dict(os.environ, {"HTTP_PROXY": "http://env-http-proxy.com"})
    @patch.dict(os.environ, {"HTTPS_PROXY": "http://env-https-proxy.com"})
    def test_proxy_precedence(self, fake_client):
        https_proxy = "https://env-https-proxy.com"

        # Verify HTTPS_PROXY takes precedence over HTTP_PROXY
        assert fake_client.configuration.proxy == https_proxy
