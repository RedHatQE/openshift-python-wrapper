from ocp_resources.resource import NamespacedResource


class TektonTasks(NamespacedResource):
    """
    TektonTasks (a Custom Resource) object, inherited from Resource.
    """

    api_group = NamespacedResource.ApiGroup.TEKTON_TASKS_KUBEVIRT_IO
