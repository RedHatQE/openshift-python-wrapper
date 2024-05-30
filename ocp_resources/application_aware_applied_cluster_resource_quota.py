# API reference: https://github.com/kubevirt/application-aware-quota/tree/main/staging/src/kubevirt.io/application-aware-quota-api/pkg/apis/core/v1alpha1
# TODO: update API reference when OCP doc is available

from ocp_resources.resource import NamespacedResource


class ApplicationAwareAppliedClusterResourceQuota(NamespacedResource):
    """
    ApplicationAwareAppliedClusterResourceQuota object.
    """

    api_group = NamespacedResource.ApiGroup.AAQ_KUBEVIRT_IO
