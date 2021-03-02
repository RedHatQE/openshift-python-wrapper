import kubernetes
import pytest
from openshift.dynamic import DynamicClient

from ocp_resources.namespace import Namespace
from ocp_resources.pod import Pod
from ocp_resources.virtual_machine import VirtualMachine
from tests.utils import generate_yaml_from_template


@pytest.fixture(scope="session")
def client():
    return DynamicClient(client=kubernetes.config.new_client_from_config())


@pytest.fixture(scope="session")
def namespace():
    with Namespace(name="namespace-for-tests") as ns:
        yield ns


def test_get(client):
    Pod.get(dyn_client=client)


def test_create():
    with Namespace(name="test-namespace"):
        pass


def test_vm(namespace):
    name = "test-vm"
    with VirtualMachine(
        name=name, namespace=namespace.name, body=generate_yaml_from_template(name=name)
    ):
        pass
