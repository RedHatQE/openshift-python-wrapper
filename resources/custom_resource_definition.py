from .resource import Resource


class CustomResourceDefinition(Resource):
    api_group = "apiextensions.k8s.io"
