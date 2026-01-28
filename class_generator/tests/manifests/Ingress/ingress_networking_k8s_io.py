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
            default_backend (dict[str, Any]): IngressBackend describes all endpoints for a given service and port.

            ingress_class_name (str): ingressClassName is the name of an IngressClass cluster resource.
              Ingress controller implementations use this field to know whether
              they should be serving this Ingress resource, by a transitive
              connection (controller -> IngressClass -> Ingress resource).
              Although the `kubernetes.io/ingress.class` annotation (simple
              constant name) was never formally defined, it was widely supported
              by Ingress controllers to create a direct binding between Ingress
              controller and Ingress resources. Newly created Ingress resources
              should prefer using the field. However, even though the annotation
              is officially deprecated, for backwards compatibility reasons,
              ingress controllers should still honor that annotation if present.

            rules (list[Any]): rules is a list of host rules used to configure the Ingress. If
              unspecified, or no rule matches, all traffic is sent to the
              default backend.

            tls (list[Any]): tls represents the TLS configuration. Currently the Ingress only
              supports a single TLS port, 443. If multiple members of this list
              specify different hosts, they will be multiplexed on the same port
              according to the hostname specified through the SNI TLS extension,
              if the ingress controller fulfilling the ingress supports SNI.

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
