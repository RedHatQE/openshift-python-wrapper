from ocp_resources.resource import NamespacedResource


class ObservabilityAddon(NamespacedResource):
    """
    https://github.com/stolostron/multicluster-observability-operator/blob/main/docs/MultiClusterObservability-CRD.md
    """

    api_group = NamespacedResource.ApiGroup.OBSERVABILITY_ADDON_IO
