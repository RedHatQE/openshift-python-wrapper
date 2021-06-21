from ocp_resources.resource import NamespacedResource


class OperatorGroup(NamespacedResource):
    api_group = NamespacedResource.ApiGroup.OPERATORS_COREOS_COM

    def __init__(
        self,
        name,
        namespace,
        target_namespaces,
        teardown=True,
        client=None,
    ):
        """
        Args:
            target_namespaces(list): namespaces in which to generate required RBAC access for its member Operators.
        """
        super().__init__(
            name=name, namespace=namespace, client=client, teardown=teardown
        )
        self.target_namespaces = target_namespaces

    def to_dict(self):
        res = super().to_dict()
        res.update({"spec": {"targetNamespaces": self.target_namespaces}})
        return res
