# -*- coding: utf-8 -*-

from ocp_resources.resource import NamespacedResource


class PeerAuthentication(NamespacedResource):
    """
    Peer Authentication object.
    """

    api_group = NamespacedResource.ApiGroup.SECURITY_ISTIO_IO

    class MtlsMode:
        """
        mTLS Traffic Mode object.
        """

        STRICT = "STRICT"
