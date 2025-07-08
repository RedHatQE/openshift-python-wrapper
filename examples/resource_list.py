"""
openshift-python-wrapper allows the creation of several similar resources at the same time
by using the ResourceList and NamespacedResourceList classes.
When used as a contextmanager, deployment and deletion is handled automatically like in other classes.
"""

import pytest
from kubernetes.dynamic import DynamicClient

from ocp_resources.namespace import Namespace
from ocp_resources.resource import get_client, ResourceList, NamespacedResourceList
from ocp_resources.role import Role


@pytest.fixture(scope="session")
def admin_client() -> DynamicClient:
    return get_client()


@pytest.fixture()
def namespaces(admin_client):
    # We create three namespaces with names: ns-1, ns-2, ns-3
    with ResourceList(resource_class=Namespace, num_resources=3, client=admin_client, name="ns") as namespaces:
        yield namespaces


@pytest.fixture()
def roles(admin_client, namespaces):
    # Given our list of namespaces, we create a Role on each namespace.
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
