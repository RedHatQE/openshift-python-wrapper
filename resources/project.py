from resources.utils import nudge_delete

from .resource import Resource


class Project(Resource):
    """
    Project object.
    This is openshift's object which represents Namespace
    """

    api_group = Resource.ApiGroup.PROJECT_OPENSHIFT_IO

    class Status(Resource.Status):
        ACTIVE = "Active"

    def nudge_delete(self):
        nudge_delete(name=self.name)


class ProjectRequest(Resource):
    """
    RequestProject object.
    Resource which adds Project and grand
    full access to user who originated this request
    """

    api_group = Resource.ApiGroup.PROJECT_OPENSHIFT_IO

    def clean_up(self):
        Project(name=self.name).delete(wait=True)
