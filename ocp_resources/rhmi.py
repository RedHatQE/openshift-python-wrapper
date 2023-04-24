from ocp_resources.resource import NamespacedResource


class RHMI(NamespacedResource):
    """
    RHMI custom resource created by Red Hat Openshift API Management (RHOAM)
    https://github.com/integr8ly/integreatly-operator/blob/master/apis/v1alpha1/rhmi_types.go
    """

    api_group = NamespacedResource.ApiGroup.INTEGREATLY_ORG
