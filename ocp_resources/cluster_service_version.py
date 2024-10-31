import json
from typing import List, Any, Dict

from ocp_resources.resource import NamespacedResource


class ClusterServiceVersion(NamespacedResource):
    api_group = NamespacedResource.ApiGroup.OPERATORS_COREOS_COM

    class Status(NamespacedResource.Status):
        INSTALLING = "Installing"

    def get_alm_examples(self) -> List[Dict[str, Any]]:
        """
        Parse the alm-examples annotation from the CSV instance and return a list of dictionaries.
        Returns an empty list if no annotation is found or if the JSON is invalid.

        Returns:
            Union[List[Dict[str, Any]], List[]]: A list of dictionaries from alm-examples, or an empty list if parsing fails.
        """
        alm_examples = self.instance.metadata.annotations.get("alm-examples")

        if not alm_examples:
            self.logger.debug(f"No alm-examples annotation found in CSV {self.name}")
            return []

        try:
            return json.loads(alm_examples)
        except json.JSONDecodeError:
            self.logger.error(f"Failed to parse alm-examples annotation from CSV {self.name}: Invalid JSON format")
            return []
