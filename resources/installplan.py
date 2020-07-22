from resources.resource import NamespacedResource


class InstallPlan(NamespacedResource):
    api_group = "operators.coreos.com"

    class Status(NamespacedResource.Status):
        COMPLETE = "Complete"
