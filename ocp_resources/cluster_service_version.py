import json

from ocp_resources.resource import NamespacedResource


class ClusterServiceVersion(NamespacedResource):
    api_group = NamespacedResource.ApiGroup.OPERATORS_COREOS_COM

    class Status(NamespacedResource.Status):
        INSTALLING = "Installing"

    import json

    def get_dict_from_examples(self):
        """
        Parse the alm-examples annotation from the CSV instance and return a list of dictionaries.

        Returns:
            List[Dict[str, str]]: A list of dictionaries, each representing a different kind from alm-examples
        """

        examples_str = self.instance.metadata.annotations["alm-examples"]
        return json.loads(examples_str)