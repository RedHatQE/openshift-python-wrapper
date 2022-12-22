from ocp_resources.role import Role


# The example bellow is also relevant for the ClusterRole resource.
# Add multiple rules to a specific Role or ClusterRole as a list of rules dictionaries:
rules = [
    {
        "api_groups": ["kubevirt.io"],
        "permissions_to_resources": ["virtualmachineinstances"],
        "verbs": ["get", "create", "delete"],
    },
    {
        "api_groups": ["subresources.kubevirt.io"],
        "permissions_to_resources": ["virtualmachineinstances/console"],
        "verbs": ["get"],
    },
    {
        "api_groups": ["k8s.cni.cncf.io"],
        "permissions_to_resources": ["network-attachment-definitions"],
        "verbs": ["get"],
    },
]
latency_role = Role(
    name="latency-role",
    namespace="namespace_name",
    rules=rules,
)
latency_role.deploy()

# delete Role
latency_role.clean_up()
