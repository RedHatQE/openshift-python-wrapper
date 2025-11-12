"""
openshift-python-wrapper allows the creation of several similar resources at the same time
by using the ResourceList and NamespacedResourceList classes.
When used as a contextmanager, deployment and deletion is handled automatically like in other classes.
"""

from ocp_resources.namespace import Namespace
from ocp_resources.resource import NamespacedResourceList, ResourceList, get_client
from ocp_resources.role import Role

client = get_client()

# We create a list of three namespaces: ns-1, ns-2, ns-3
namespaces = ResourceList(resource_class=Namespace, num_resources=3, client=client, name="ns")
namespaces.deploy()

assert namespaces[2].name == "ns-3"

# Now we create one role on each namespace
roles = NamespacedResourceList(
    client=client,
    resource_class=Role,
    name="role",
    namespaces=[ns.name for ns in namespaces],
    rules=[
        {
            "apiGroups": ["serving.kserve.io"],
            "resources": ["inferenceservices"],
            "verbs": ["get", "list", "watch"],
        }
    ],
)

assert roles[2].namespace == "ns-3"

# We clean up all the resources we created
namespaces.clean_up()
roles.clean_up()


# We can also work with these classes using contextmanagers
# for automatic clean up
with ResourceList(client=client, resource_class=Namespace, name="ns", num_resources=3) as namespaces:
    assert namespaces[0].name == "ns-1"
