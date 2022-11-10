from ocp_resources.resource import Resource


class NodeHealthCheck(Resource):
    """
    NodeHealthCheck object.
    Reference : https://github.com/medik8s/node-healthcheck-operator
    """

    api_group = Resource.ApiGroup.REMEDIATION_MEDIK8S_IO
