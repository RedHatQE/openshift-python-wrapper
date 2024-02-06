import kubernetes
import pytest
from kubernetes.dynamic import DynamicClient

from ocp_resources.namespace import Namespace
from ocp_resources.virtual_machine import VirtualMachine
from tests.utils import generate_yaml_from_template


@pytest.fixture(scope="session")
def client():
    return DynamicClient(client=kubernetes.config.new_client_from_config())


@pytest.fixture(scope="session")
def namespace():
    return Namespace(name="test-namespace")


@pytest.mark.incremental
class TestNamespace:
    def test_create(self, namespace):
        namespace.create()

    def test_wait(self, namespace):
        namespace.wait_for_status(status=Namespace.Status.ACTIVE, timeout=30)

    def test_get(self, client, namespace):
        Namespace.get(name=namespace.name, dyn_client=client)

    def test_delete(self, namespace):
        namespace.delete(wait=True)


@pytest.mark.kubevirt
def test_vm(namespace):
    name = "test-vm"
    with VirtualMachine(name=name, namespace=namespace.name, body=generate_yaml_from_template(name=name)):
        pass
