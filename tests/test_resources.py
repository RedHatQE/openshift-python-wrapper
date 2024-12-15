import pytest

from ocp_resources.namespace import Namespace
from ocp_resources.pod import Pod
from ocp_resources.resource import Resource, get_client
import yaml
from testcontainers.k3s import K3SContainer


@pytest.fixture(scope="session")
def client():
    with K3SContainer() as k3s:
        yield get_client(config_dict=yaml.safe_load(k3s.config_yaml()))


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
