from ocp_resources.resource import Resource


class TektonTasks(Resource):
    """
    TektonTasks (a Custom Resource) object, inherited from Resource.
    """

    api_group = Resource.ApiGroup.TEKTON_TASKS_KUBEVIRT_IO
