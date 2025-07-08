import time
import pytest
from kubernetes.dynamic import DynamicClient

from ocp_resources.namespace import Namespace
from ocp_resources.resource import ResourceList, get_client, NamespacedResourceList
from ocp_resources.role import Role


@pytest.fixture(scope="session")
def admin_client() -> DynamicClient:
    return get_client()


@pytest.fixture()
def namespaces(admin_client):
    with ResourceList(resource_class=Namespace, num_resources=3, client=admin_client, name="ns") as namespaces:
        yield namespaces


@pytest.fixture()
def roles(admin_client, namespaces):
    rules = [
        {
            "apiGroups": ["serving.kserve.io"],
            "resources": ["inferenceservices"],
            "verbs": ["get", "list", "watch"],
        }
    ]
    with NamespacedResourceList(
        client=admin_client,
        resource_class=Role,
        name="role",
        namespaces=[ns.name for ns in namespaces.resources],
        rules=rules,
    ) as roles:
        yield roles


def test_dummy(namespaces, roles):
    for role in roles.resources:
        print(role.name)
        print(role.rules)
        print(role.namespace)

    time.sleep(120)
