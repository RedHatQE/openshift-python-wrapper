# API reference:
#       https://docs.openshift.com/container-platform/4.12/rest_api/config_apis/dns-config-openshift-io-v1.html

from ocp_resources.resource import Resource


class DNS(Resource):
    """
    DNS object.
    """

    api_group = Resource.ApiGroup.CONFIG_OPENSHIFT_IO
