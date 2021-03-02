from ocp_resources.resource import NamespacedResource


class InstallPlan(NamespacedResource):
    api_group = NamespacedResource.ApiGroup.OPERATORS_COREOS_COM

    class Status(NamespacedResource.Status):
        COMPLETE = "Complete"
