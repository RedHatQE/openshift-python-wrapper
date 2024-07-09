# -*- coding: utf-8 -*-
from ocp_resources.constants import TIMEOUT_4MINUTES
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
        delete_timeout=TIMEOUT_4MINUTES,
        **kwargs,
    ):
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            teardown=teardown,
            yaml_file=yaml_file,
            delete_timeout=delete_timeout,
            **kwargs,
        )
        self.service = service
        self.destination_ca_cert = destination_ca_cert

    def to_dict(self) -> None:
        super().to_dict()
        if not self.yaml_file:
            if self.service:
                self.res.update({"spec": {"to": {"kind": "Service", "name": self.service}}})
            if self.destination_ca_cert:
                self.res["spec"]["tls"] = {
                    "destinationCACertificate": self.destination_ca_cert,
                    "termination": "reencrypt",
                }

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
