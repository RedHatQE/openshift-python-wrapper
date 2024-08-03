# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, List, Optional
from ocp_resources.resource import NamespacedResource


class Machine(NamespacedResource):
    """
    Machine is the Schema for the machines API Compatibility level 2: Stable
    within a major release for a minimum of 9 months or 3 minor releases
    (whichever is longer).
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
            lifecycle_hooks(Dict[Any, Any]): LifecycleHooks allow users to pause operations on the machine at certain
              predefined points within the machine lifecycle.

              FIELDS:
                preDrain	<[]Object>
                  PreDrain hooks prevent the machine from being drained. This also blocks
                  further lifecycle events, such as termination.

                preTerminate	<[]Object>
                  PreTerminate hooks prevent the machine from being terminated. PreTerminate
                  hooks be actioned after the Machine has been drained.

            metadata(Dict[Any, Any]): ObjectMeta will autopopulate the Node created. Use this to indicate what
              labels, annotations, name prefix, etc., should be used when creating the
              Node.

              FIELDS:
                annotations	<map[string]string>
                  Annotations is an unstructured key value map stored with a resource that may
                  be set by external tools to store and retrieve arbitrary metadata. They are
                  not queryable and should be preserved when modifying objects. More info:
                  http://kubernetes.io/docs/user-guide/annotations

                generateName	<string>
                  GenerateName is an optional prefix, used by the server, to generate a unique
                  name ONLY IF the Name field has not been provided. If this field is used,
                  the name returned to the client will be different than the name passed. This
                  value will also be combined with a unique suffix. The provided value has the
                  same validation rules as the Name field, and may be truncated by the length
                  of the suffix required to make the value unique on the server.
                   If this field is specified and the generated name exists, the server will
                  NOT return a 409 - instead, it will either return 201 Created or 500 with
                  Reason ServerTimeout indicating a unique name could not be found in the time
                  allotted, and the client should retry (optionally after the time indicated
                  in the Retry-After header).
                   Applied only if Name is not specified. More info:
                  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#idempotency

                labels	<map[string]string>
                  Map of string keys and values that can be used to organize and categorize
                  (scope and select) objects. May match selectors of replication controllers
                  and services. More info: http://kubernetes.io/docs/user-guide/labels

                name	<string>
                  Name must be unique within a namespace. Is required when creating resources,
                  although some resources may allow a client to request the generation of an
                  appropriate name automatically. Name is primarily intended for creation
                  idempotence and configuration definition. Cannot be updated. More info:
                  http://kubernetes.io/docs/user-guide/identifiers#names

                namespace	<string>
                  Namespace defines the space within each name must be unique. An empty
                  namespace is equivalent to the "default" namespace, but "default" is the
                  canonical representation. Not all objects are required to be scoped to a
                  namespace - the value of this field for those objects will be empty.
                   Must be a DNS_LABEL. Cannot be updated. More info:
                  http://kubernetes.io/docs/user-guide/namespaces

                ownerReferences	<[]Object>
                  List of objects depended by this object. If ALL objects in the list have
                  been deleted, this object will be garbage collected. If this object is
                  managed by a controller, then an entry in this list will point to this
                  controller, with the controller field set to true. There cannot be more than
                  one managing controller.

            provider_id(str): ProviderID is the identification ID of the machine provided by the provider.
              This field must match the provider ID as seen on the node object
              corresponding to this machine. This field is required by higher level
              consumers of cluster-api. Example use case is cluster autoscaler with
              cluster-api as provider. Clean-up logic in the autoscaler compares machines
              to nodes to find out machines at provider which could not get registered as
              Kubernetes nodes. With cluster-api as a generic out-of-tree provider for
              autoscaler, this field is required by autoscaler to be able to have a
              provider view of the list of machines. Another list of nodes is queried from
              the k8s apiserver and then a comparison is done to find out unregistered
              machines and are marked for delete. This field will be set by the actuators
              and consumed by higher level entities like autoscaler that will be
              interfacing with cluster-api as generic provider.

            provider_spec(Dict[Any, Any]): ProviderSpec details Provider-specific configuration to use during node
              creation.

              FIELDS:
                value	<Object>
                  Value is an inlined, serialized representation of the resource
                  configuration. It is recommended that providers maintain their own versioned
                  API types that should be serialized/deserialized from this field, akin to
                  component config.

            taints(List[Any]): The list of the taints to be applied to the corresponding Node in additive
              manner. This list will not overwrite any other taints added to the Node on
              an ongoing basis by other entities. These taints should be actively
              reconciled e.g. if you ask the machine controller to apply a taint and then
              manually remove the taint the machine controller will put it back) but not
              have the machine controller remove any taints
              The node this Taint is attached to has the "effect" on any pod that does not
              tolerate the Taint.

              FIELDS:
                effect	<string> -required-
                  Required. The effect of the taint on pods that do not tolerate the taint.
                  Valid effects are NoSchedule, PreferNoSchedule and NoExecute.

                key	<string> -required-
                  Required. The taint key to be applied to a node.

                timeAdded	<string>
                  TimeAdded represents the time at which the taint was added. It is only
                  written for NoExecute taints.

                value	<string>
                  The taint value corresponding to the taint key.

        """
        super().__init__(**kwargs)

        self.lifecycle_hooks = lifecycle_hooks
        self.metadata = metadata
        self.provider_id = provider_id
        self.provider_spec = provider_spec
        self.taints = taints

    def to_dict(self) -> None:
        super().to_dict()

        if not self.yaml_file:
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

    @property
    def cluster_name(self):
        return self.instance.metadata.labels[f"{self.api_group}/cluster-api-cluster"]

    @property
    def machine_role(self):
        return self.instance.metadata.labels[f"{self.api_group}/cluster-api-machine-role"]

    @property
    def machine_type(self):
        return self.instance.metadata.labels[f"{self.api_group}/cluster-api-machine-type"]

    @property
    def machineset_name(self):
        return self.instance.metadata.labels[f"{self.api_group}/cluster-api-machineset"]
