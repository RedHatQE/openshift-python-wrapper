# -*- coding: utf-8 -*-

from ocp_resources.resource import NamespacedResource


class Route(NamespacedResource):
    """
    OpenShift Route object.
    """

    api_group = NamespacedResource.ApiGroup.ROUTE_OPENSHIFT_IO

    def __init__(
        self,
        name=None,
        namespace=None,
        client=None,
        service=None,
        destination_ca_cert=None,
        teardown=True,
        yaml_file=None,
    ):
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            teardown=teardown,
            yaml_file=yaml_file,
        )
        self.service = service
        self.destination_ca_cert = destination_ca_cert

    def to_dict(self):
        res = super().to_dict()
        if self.yaml_file:
            return res

        if self.service:
            res.update({"spec": {"to": {"kind": "Service", "name": self.service}}})
        if self.destination_ca_cert:
            res["spec"]["tls"] = {
                "destinationCACertificate": self.destination_ca_cert,
                "termination": "reencrypt",
            }
        return res

    @property
    def exposed_service(self):
        """
        returns the service the route is exposing
        """
        return self.instance.spec.to.name

    @property
    def host(self):
        """
        returns hostname that is exposing the service
        """
        return self.instance.spec.host

    @property
    def ca_cert(self):
        """
        returns destinationCACertificate
        """
        return self.instance.spec.tls.destinationCACertificate

    @property
    def termination(self):
        """
        returns a secured route using re-encrypt termination
        """
        return self.instance.spec.tls.termination
