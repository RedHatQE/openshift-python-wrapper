# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, List, Optional
from ocp_resources.resource import NamespacedResource


class Service(NamespacedResource):
    """
       Service acts as a top-level container that manages a Route and Configuration which implement a network service. Service exists to provide a singular abstraction which can be access controlled, reasoned about, and which encapsulates software lifecycle decisions such as rollout policy and team resource ownership. Service acts only as an orchestrator of the underlying Routes and Configurations (much as a kubernetes Deployment orchestrates ReplicaSets), and its usage is optional but recommended.
    The Service's controller will track the statuses of its owned Configuration and Route, reflecting their statuses and conditions as its own.
    See also: https://github.com/knative/serving/blob/main/docs/spec/overview.md#service
    """

    api_group: str = NamespacedResource.ApiGroup.SERVING_KNATIVE_DEV

    def __init__(
        self,
        template: Optional[Dict[str, Any]] = None,
        traffic: Optional[List[Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            template (Dict[str, Any]): Template holds the latest specification for the Revision to be stamped
              out.

            traffic (List[Any]): Traffic specifies how to distribute traffic over a collection of
              revisions and configurations.

        """
        super().__init__(**kwargs)

        self.template = template
        self.traffic = traffic

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.template:
                _spec["template"] = self.template

            if self.traffic:
                _spec["traffic"] = self.traffic

    # End of generated code
