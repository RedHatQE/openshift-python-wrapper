from ocp_resources.resource import NamespacedResource


class NodeHealthCheck(NamespacedResource):
    """
    NodeHealthCheck object.
    Reference : https://github.com/medik8s/node-healthcheck-operator
    """

    api_group = NamespacedResource.ApiGroup.REMEDIATION_MEDIK8S_IO
