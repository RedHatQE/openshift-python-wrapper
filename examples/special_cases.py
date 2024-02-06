"""
Some resources have the same `kind` but different API groups.
For example: `Network` which exists in both operator.openshift.io and config.openshift.io API groups
"""

from ocp_resources.network import Network

# To get the Network resource which uses the default API in the class ("config.openshift.io")
Network(name="cluster")

# To get a Network resource with a different API group ("operator.openshift.io")
Network(name="cluster", api_group=Network.ApiGroup.OPERATOR_OPENSHIFT_IO)
