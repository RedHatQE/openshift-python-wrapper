from resources.resource import NamespacedResource


class OperatorGroup(NamespacedResource):
    api_group = "operators.coreos.com"

    def __init__(
        self, name, namespace, target_namespaces, teardown=False,
    ):
        """
        Args:
            target_namespaces(list): namespaces in which to generate required RBAC access for its member Operators.
        """
        super().__init__(name=name, namespace=namespace, teardown=teardown)
        self.target_namespaces = target_namespaces

    def to_dict(self):
        res = super()._base_body()
        res.update({"spec": {"targetNamespaces": self.target_namespaces}})
        return res
