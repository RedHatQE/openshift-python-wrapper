from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.resource import Resource


class Project(Resource):
    """
    Project object.
    This is openshift's object which represents Namespace
    """

    api_group = Resource.ApiGroup.PROJECT_OPENSHIFT_IO

    class Status(Resource.Status):
        ACTIVE = "Active"

    def clean_up(self):
        Project(name=self.name).delete(wait=True)


class ProjectRequest(Resource):
    """
    RequestProject object.
    Resource which adds Project and grand
    full access to user who originated this request
    """

    api_group = Resource.ApiGroup.PROJECT_OPENSHIFT_IO

    def __init__(
        self,
        name=None,
        client=None,
        teardown=True,
        timeout=TIMEOUT_4MINUTES,
        yaml_file=None,
        delete_timeout=TIMEOUT_4MINUTES,
        **kwargs,
    ):
        super().__init__(
            name=name,
            client=client,
            teardown=teardown,
            timeout=timeout,
            yaml_file=yaml_file,
            delete_timeout=delete_timeout,
            **kwargs,
        )

    def clean_up(self):
        Project(name=self.name).delete(wait=True)

    def client_wait_deleted(self, timeout):
        """
        client-side Wait until resource is deleted

        Args:
            timeout (int): Time to wait for the resource.

        """
        super().client_wait_deleted(timeout=timeout)
