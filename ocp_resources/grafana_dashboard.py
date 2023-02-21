from ocp_resources.resource import NamespacedResource


class GrafanaDashboard(NamespacedResource):
    """
    GrafanaDashboard Resource. API Reference:
    https://github.com/grafana-operator/grafana-operator/blob/master/documentation/api.md
    """

    api_group = NamespacedResource.ApiGroup.INTEGREATLY_ORG

    def __init__(
        self,
        name=None,
        namespace=None,
        label=None,
        configmap_name=None,
        configmap_key=None,
        data_sources=None,
        yaml_file=None,
        **kwargs
    ):
        """

        Args:
            name (str): Resource name
            namespace (str): Resource namespace
            label (dict): Resource labels (Used by Grafana to identify GrafanaDashboards)
            configmap_name (str): Name of ConfigMap containing dashboard JSON
            configmap_key (str): Key in ConfigMap referencing dashboard JSON
            data_sources (list): List of data sources
            yaml_file (str): yaml file for the resource (in lieu of other arguments)

        Example:
            GrafanaDashboard(
                name="dashboard",
                namespace="grafana",
                label={"app": "grafana"},
                configmap_name="my_dashboard_configmap",
                configmap_key="dashboard_1",
                data_sources=[{"inputName": "DS_PROMETHEUS", "datasourceName": "Prometheus"}]
            )

        """
        super().__init__(name=name, namespace=namespace, yaml_file=yaml_file, **kwargs)
        self.label = label
        self.configmap_name = configmap_name
        self.configmap_key = configmap_key
        self.data_sources = data_sources

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file:
            self.res.update(
                {
                    "metadata": {
                        "labels": self.label,
                    },
                    "spec": {
                        "json": "",
                        "configMapRef": {
                            "name": self.configmap_name,
                            "key": self.configmap_key,
                        },
                        "datasources": self.data_sources,
                    },
                }
            )
