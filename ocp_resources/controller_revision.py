from ocp_resources.resource import NamespacedResource


class ControllerRevision(NamespacedResource):
    api_group = NamespacedResource.ApiGroup.APPS
