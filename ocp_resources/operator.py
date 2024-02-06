# https://docs.openshift.com/container-platform/4.12/operators/operator-reference.html

from ocp_resources.resource import Resource


class Operator(Resource):
    api_group = Resource.ApiGroup.OPERATORS_COREOS_COM
