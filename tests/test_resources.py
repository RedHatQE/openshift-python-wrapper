from __future__ import annotations

import os
from unittest.mock import patch

import pytest
import yaml
from docker.errors import DockerException
from testcontainers.k3s import K3SContainer

from ocp_resources.exceptions import ResourceTeardownError
from ocp_resources.namespace import Namespace
from ocp_resources.pod import Pod
from ocp_resources.resource import Resource, get_client
from ocp_resources.secret import Secret


class SecretTestExit(Secret):
    def deploy(self, wait: bool = False):
        return self

    def clean_up(self, wait: bool = True, timeout: int | None = None) -> bool:
        return False


@pytest.fixture(scope="class")
def k3scontainer_config():
    try:
        with K3SContainer() as k3s:
            yield yaml.safe_load(k3s.config_yaml())
    except DockerException as ex:
        pytest.skip(f"K3S container not available. {ex}")


@pytest.fixture(scope="class")
def client(k3scontainer_config):
    yield get_client(config_dict=k3scontainer_config)


@pytest.fixture(scope="class")
def namespace(client):
    return Namespace(client=client, name="test-namespace")


@pytest.fixture(scope="class")
def pod(client):
    yield list(Pod.get(dyn_client=client))[0]


@pytest.mark.incremental
class TestResource:
    def test_get(self, client):
        for ns in Namespace.get(dyn_client=client):
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

    def test_get_all_cluster_resources(self, client):
        for _resources in Resource.get_all_cluster_resources(client=client):
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

    def test_resource_context_manager(self, client):
        with Secret(name="test-context-manager", namespace="default", client=client) as sec:
            pass

        assert not sec.exists

    def test_resource_context_manager_exit(self, client):
        with pytest.raises(ResourceTeardownError):
            with SecretTestExit(name="test-context-manager-exit", namespace="default", client=client):
                pass


@pytest.mark.xfail(reason="Need debug")
class TestClientProxy:
    @patch.dict(os.environ, {"HTTP_PROXY": "http://env-http-proxy.com"})
    def test_client_with_proxy(self, k3scontainer_config):
        http_proxy = "http://env-http-proxy.com"

        client = get_client(config_dict=k3scontainer_config)
        assert client.configuration.proxy == http_proxy

    @patch.dict(os.environ, {"HTTP_PROXY": "http://env-http-proxy.com"})
    @patch.dict(os.environ, {"HTTPS_PROXY": "http://env-http-proxy.com"})
    def test_proxy_precedence(self, k3scontainer_config):
        https_proxy = "https://env-https-proxy.com"

        client = get_client(config_dict=k3scontainer_config)
        # Verify HTTPS_PROXY takes precedence over HTTP_PROXY
        assert client.configuration.proxy == https_proxy
