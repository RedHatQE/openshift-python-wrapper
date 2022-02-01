from ocp_resources.resource import NamespacedResource


class Job(NamespacedResource):
    """
    Job object.
    """

    api_group = NamespacedResource.ApiGroup.BATCH
