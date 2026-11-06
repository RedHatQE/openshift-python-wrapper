"""
Some resources have the same `kind` but different API groups.
For example: `Network` which exists in both operator.openshift.io and config.openshift.io API groups
"""

from ocp_resources.network_config_openshift_io import Network
from ocp_resources.resource import get_client

client = get_client()

# To get the Network resource which uses the default API in the class ("config.openshift.io")
Network(client=client, name="cluster")

# To get a Network resource with a different API group ("operator.openshift.io")
Network(client=client, name="cluster", api_group=Network.ApiGroup.OPERATOR_OPENSHIFT_IO)
