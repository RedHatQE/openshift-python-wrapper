# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import Resource


class Ingress(Resource):
    """
    Ingress is a collection of rules that allow inbound connections to reach the endpoints defined by a backend. An Ingress can be configured to give services externally-reachable urls, load balance traffic, terminate SSL, offer name based virtual hosting etc.
    """

    api_group: str = Resource.ApiGroup.NETWORKING_K8S_IO

    def __init__(
        self,
        default_backend: dict[str, Any] | None = None,
        ingress_class_name: str | None = None,
        rules: list[Any] | None = None,
        tls: list[Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            default_backend (dict[str, Any]): resource apiGroup kind name service name port name number.

            ingress_class_name (str): No field description from API

            rules (list[Any]): host http paths backend resource apiGroup kind name service name port
              name number path pathType enum: Exact, ImplementationSpecific,
              Prefix.

            tls (list[Any]): hosts secretName.

        """
        super().__init__(**kwargs)

        self.default_backend = default_backend
        self.ingress_class_name = ingress_class_name
        self.rules = rules
        self.tls = tls

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.default_backend is not None:
                _spec["defaultBackend"] = self.default_backend

            if self.ingress_class_name is not None:
                _spec["ingressClassName"] = self.ingress_class_name

            if self.rules is not None:
                _spec["rules"] = self.rules

            if self.tls is not None:
                _spec["tls"] = self.tls

    # End of generated code
