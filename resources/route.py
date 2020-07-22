# -*- coding: utf-8 -*-
import logging

from .resource import NamespacedResource


LOGGER = logging.getLogger(__name__)


class Route(NamespacedResource):
    """
    OpenShift Route object.
    """

    api_group = "route.openshift.io"

    def __init__(
        self, name, namespace, service=None, destination_ca_cert=None, teardown=True
    ):
        super().__init__(name=name, namespace=namespace, teardown=teardown)
        self.service = service
        self.destination_ca_cert = destination_ca_cert

    def to_dict(self):
        body = super()._base_body()
        if self.service:
            body.update({"spec": {"to": {"kind": "Service", "name": self.service}}})
        if self.destination_ca_cert:
            body["spec"]["tls"] = {
                "destinationCACertificate": self.destination_ca_cert,
                "termination": "reencrypt",
            }
        return body

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
