from ocp_resources.resource import NamespacedResource


class OperatorCondition(NamespacedResource):
    api_group = NamespacedResource.ApiGroup.OPERATORS_COREOS_COM
