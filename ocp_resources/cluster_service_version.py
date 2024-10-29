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

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each representing a different kind from alm-examples
        """

        examples = self.instance.metadata.annotations.get("alm-examples")
        return json.loads(examples) if examples else None
