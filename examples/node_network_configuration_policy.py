from ocp_resources.node_network_configuration_policy import (
    NodeNetworkConfigurationPolicy,
)

# Using capture syntax to switch ipv4 config between interfaces
my_nncp = NodeNetworkConfigurationPolicy(
    name="capture_nncp",
    capture={
        "first-nic": 'interfaces.name=="ens8"',
        "second-nic": 'interfaces.name=="ens9"',
    },
)
my_nncp.deploy()
my_nncp.add_interface(
    name="{{ capture.first-nic.interfaces.0.name }}",
    set_ipv4="{{ capture.second-nic.interfaces.0.ipv4 }}",
)
my_nncp.add_interface(
    name="{{ capture.second-nic.interfaces.0.name }}",
    set_ipv4="{{ capture.first-nic.interfaces.0.ipv4 }}",
)

# delete NNCP
my_nncp.clean_up()
