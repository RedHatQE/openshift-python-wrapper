# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, List, Optional
from ocp_resources.resource import NamespacedResource


class Machine(NamespacedResource):
    """
    Machine is the Schema for the machines API Compatibility level 2: Stable within a major release for a minimum of 9 months or 3 minor releases (whichever is longer).
    """

    api_group: str = NamespacedResource.ApiGroup.MACHINE_OPENSHIFT_IO

    def __init__(
        self,
        lifecycle_hooks: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        provider_id: Optional[str] = "",
        provider_spec: Optional[Dict[str, Any]] = None,
        taints: Optional[List[Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            lifecycle_hooks (Dict[str, Any]): LifecycleHooks allow users to pause operations on the machine at
              certain predefined points within the machine lifecycle.

            metadata (Dict[str, Any]): ObjectMeta will autopopulate the Node created. Use this to indicate
              what labels, annotations, name prefix, etc., should be used when
              creating the Node.

            provider_id (str): ProviderID is the identification ID of the machine provided by the
              provider. This field must match the provider ID as seen on the
              node object corresponding to this machine. This field is required
              by higher level consumers of cluster-api. Example use case is
              cluster autoscaler with cluster-api as provider. Clean-up logic in
              the autoscaler compares machines to nodes to find out machines at
              provider which could not get registered as Kubernetes nodes. With
              cluster-api as a generic out-of-tree provider for autoscaler, this
              field is required by autoscaler to be able to have a provider view
              of the list of machines. Another list of nodes is queried from the
              k8s apiserver and then a comparison is done to find out
              unregistered machines and are marked for delete. This field will
              be set by the actuators and consumed by higher level entities like
              autoscaler that will be interfacing with cluster-api as generic
              provider.

            provider_spec (Dict[str, Any]): ProviderSpec details Provider-specific configuration to use during
              node creation.

            taints (List[Any]): The list of the taints to be applied to the corresponding Node in
              additive manner. This list will not overwrite any other taints
              added to the Node on an ongoing basis by other entities. These
              taints should be actively reconciled e.g. if you ask the machine
              controller to apply a taint and then manually remove the taint the
              machine controller will put it back) but not have the machine
              controller remove any taints

        """
        super().__init__(**kwargs)

        self.lifecycle_hooks = lifecycle_hooks
        self.metadata = metadata
        self.provider_id = provider_id
        self.provider_spec = provider_spec
        self.taints = taints

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.lifecycle_hooks:
                _spec["lifecycleHooks"] = self.lifecycle_hooks

            if self.metadata:
                _spec["metadata"] = self.metadata

            if self.provider_id:
                _spec["providerID"] = self.provider_id

            if self.provider_spec:
                _spec["providerSpec"] = self.provider_spec

            if self.taints:
                _spec["taints"] = self.taints

    # End of generated code
