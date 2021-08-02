from ocp_resources.resource import TIMEOUT, Resource


class Project(Resource):
    """
    Project object.
    This is openshift's object which represents Namespace
    """

    api_group = Resource.ApiGroup.PROJECT_OPENSHIFT_IO

    class Status(Resource.Status):
        ACTIVE = "Active"


class ProjectRequest(Resource):
    """
    RequestProject object.
    Resource which adds Project and grand
    full access to user who originated this request
    """

    api_group = Resource.ApiGroup.PROJECT_OPENSHIFT_IO

    def __init__(
        self, name=None, client=None, teardown=True, timeout=TIMEOUT, yaml_file=None
    ):
        super().__init__(
            name=name,
            client=client,
            teardown=teardown,
            timeout=timeout,
            yaml_file=yaml_file,
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
