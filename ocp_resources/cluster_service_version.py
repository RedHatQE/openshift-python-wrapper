import json
from typing import List, Any, Dict, Union

from ocp_resources.resource import NamespacedResource


class ClusterServiceVersion(NamespacedResource):
    api_group = NamespacedResource.ApiGroup.OPERATORS_COREOS_COM

    class Status(NamespacedResource.Status):
        INSTALLING = "Installing"

    def get_alm_examples(self) -> Union[List[Dict[str, Any]], List]:
        """
        Parse the alm-examples annotation from the CSV instance and return a list of dictionaries.

        Returns:
            Union[List[Dict[str, Any]], List]: Either a list of dictionaries from alm-examples,
            or an empty list if alm-examples doesn't exist.
        """
        examples = self.instance.metadata.annotations.get("alm-examples")
        if not examples:
            self.logger.debug("No alm-examples annotation found in CSV")
            return []
        try:
            return json.loads(examples)
        except json.JSONDecodeError as e:
            self.logger.warning(f"Failed to parse alm-examples annotation: {e}")
        return []
