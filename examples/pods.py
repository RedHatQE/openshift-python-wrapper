import kubernetes
from kubernetes.dynamic import DynamicClient

from ocp_resources.pod import Pod

client = DynamicClient(client=kubernetes.config.new_client_from_config())

# Query to get Pods (resource) in the connected cluster with label of ``label_example=example``.
# Returns a ``generator`` of the resource - ``pod``
for pod in Pod.get(dyn_client=client, label_selector="label_example=example"):
    # We can also get the Node that the ``pod`` is running on:
    node = pod.node  # Return instance of Node()
    # Get pod logs
    pod.log()
