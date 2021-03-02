from ocp_resources.resource import Resource


class CustomResourceDefinition(Resource):
    api_group = Resource.ApiGroup.APIEXTENSIONS_K8S_IO
