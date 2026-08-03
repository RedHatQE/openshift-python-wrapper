# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md


from typing import Any

from ocp_resources.resource import Resource


class ResourceFlavor(Resource):
    """
    ResourceFlavor is the Schema for the resourceflavors API.
    """

    api_group: str = Resource.ApiGroup.KUEUE_X_K8S_IO

    def __init__(
        self,
        node_labels: dict[str, Any] | None = None,
        node_taints: list[Any] | None = None,
        tolerations: list[Any] | None = None,
        topology_name: str | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            node_labels (dict[str, Any]): nodeLabels are labels that associate the ResourceFlavor with Nodes
              that have the same labels. When a Workload is admitted, its
              podsets can only get assigned ResourceFlavors whose nodeLabels
              match the nodeSelector and nodeAffinity fields. Once a
              ResourceFlavor is assigned to a podSet, the ResourceFlavor's
              nodeLabels should be injected into the pods of the Workload by the
              controller that integrates with the Workload object.  nodeLabels
              can be up to 8 elements.

            node_taints (list[Any]): nodeTaints are taints that the nodes associated with this
              ResourceFlavor have. Workloads' podsets must have tolerations for
              these nodeTaints in order to get assigned this ResourceFlavor
              during admission. Only the 'NoSchedule' and 'NoExecute' taint
              effects are evaluated, while 'PreferNoSchedule' is ignored.  An
              example of a nodeTaint is
              cloud.provider.com/preemptible="true":NoSchedule  nodeTaints can
              be up to 8 elements.

            tolerations (list[Any]): tolerations are extra tolerations that will be added to the pods
              admitted in the quota associated with this resource flavor.  An
              example of a toleration is
              cloud.provider.com/preemptible="true":NoSchedule  tolerations can
              be up to 8 elements.

            topology_name (str): topologyName indicates topology for the TAS ResourceFlavor. When
              specified, it enables scraping of the topology information from
              the nodes matching to the Resource Flavor node labels.

        """
        super().__init__(**kwargs)

        self.node_labels = node_labels
        self.node_taints = node_taints
        self.tolerations = tolerations
        self.topology_name = topology_name

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.node_labels is not None:
                _spec["nodeLabels"] = self.node_labels

            if self.node_taints is not None:
                _spec["nodeTaints"] = self.node_taints

            if self.tolerations is not None:
                _spec["tolerations"] = self.tolerations

            if self.topology_name is not None:
                _spec["topologyName"] = self.topology_name

    # End of generated code
