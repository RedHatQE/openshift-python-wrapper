import json

from ocp_resources.resource import NamespacedResource


class ClusterServiceVersion(NamespacedResource):
    api_group = NamespacedResource.ApiGroup.OPERATORS_COREOS_COM

    class Status(NamespacedResource.Status):
        INSTALLING = "Installing"

    import json

    def get_dicts_from_examples(self):
        """
        Parse the alm-examples annotation from the CSV instance and return a list of dictionaries.

        Returns: examples_list (List[Dict[str, str]])
        """
        try:
            examples_str = self.instance.metadata.annotations["alm-examples"]

            examples_list = json.loads(examples_str)

            return examples_list

        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return []
        except KeyError as e:
            print(f"Missing key in metadata: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error: {e}")
            return []
