from ocp_resources.resource import NamespacedResource


class GrafanaDataSource(NamespacedResource):
    """
    GrafanaDataSource Resource. API Reference:
    https://github.com/grafana-operator/grafana-operator/blob/master/documentation/api.md
    """

    api_group = NamespacedResource.ApiGroup.INTEGREATLY_ORG
