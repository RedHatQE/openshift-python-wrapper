# -*- coding: utf-8 -*-

from resources.resource import NamespacedResource


class Service(NamespacedResource):
    """
    OpenShift Service object.
    """

    api_version = NamespacedResource.ApiVersion.V1

    class Type:
        CLUSTER_IP = "ClusterIP"
        NODE_PORT = "NodePort"

    def __init__(
        self,
        name,
        namespace,
        client=None,
        teardown=True,
    ):
        super().__init__(
            name=name, namespace=namespace, client=client, teardown=teardown
        )
