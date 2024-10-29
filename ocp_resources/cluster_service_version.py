import json
from typing import List, Any

from ocp_resources.resource import NamespacedResource


class ClusterServiceVersion(NamespacedResource):
    api_group = NamespacedResource.ApiGroup.OPERATORS_COREOS_COM

    class Status(NamespacedResource.Status):
        INSTALLING = "Installing"

    def get_dicts_from_examples(self) -> List[dict[str, Any]]:
        """
        Parse the alm-examples annotation from the CSV instance and return a list of dictionaries.

        Returns:
            List[dict[str, Any]]: A list of dictionaries from alm-examples. Returns empty list if
            alm-examples doesn't exist or is invalid.
        """

        examples = self.instance.metadata.annotations.get("alm-examples")
        return json.loads(examples) if examples else []
