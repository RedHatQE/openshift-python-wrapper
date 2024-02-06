import kubernetes
from kubernetes.dynamic import DynamicClient

from ocp_resources.namespace import Namespace

client = DynamicClient(client=kubernetes.config.new_client_from_config())

# The examples given below are relevant to all resources. For simplicity we will use the resource - Namespace.

ns = Namespace(name="namespace-example-1")
ns.deploy()
assert ns.exists
ns.clean_up()

# We can also use the ``with`` statement which ensures automatic clean-up of the code executed:
# teardown=False`` -  Disables clean-up after execution
with Namespace(name="namespace-example-2") as ns:
    # Wait for Namespace to be in status ``Active``:
    # Will raise a ``TimeoutExpiredError`` if Namespace is not in the desired status.
    ns.wait_for_status(status=Namespace.Status.ACTIVE, timeout=120)
    # Checks if Namespace exists on the server:
