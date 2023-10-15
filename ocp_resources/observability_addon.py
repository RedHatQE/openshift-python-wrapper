from ocp_resources.resource import NamespacedResource


class ObservabilityAddon(NamespacedResource):
    """
    https://github.com/stolostron/multicluster-observability-operator/blob/main/docs/MultiClusterObservability-CRD.md
    """

    class Status(NamespacedResource.Status):
        AVAILABLE = "Available"

    api_group = NamespacedResource.ApiGroup.OBSERVABILITY_ADDON_IO
