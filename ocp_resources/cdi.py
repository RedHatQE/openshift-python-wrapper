# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, Optional
from ocp_resources.resource import Resource


class CDI(Resource):
    """
    CDI is the CDI Operator CRD
    """

    api_group: str = Resource.ApiGroup.CDI_KUBEVIRT_IO

    class Status(Resource.Status):
        DEPLOYING: str = "Deploying"
        DEPLOYED: str = "Deployed"

    def __init__(
        self,
        cert_config: Optional[Dict[str, Any]] = None,
        clone_strategy_override: Optional[str] = "",
        config: Optional[Dict[str, Any]] = None,
        customize_components: Optional[Dict[str, Any]] = None,
        image_pull_policy: Optional[str] = "",
        infra: Optional[Dict[str, Any]] = None,
        priority_class: Optional[str] = "",
        uninstall_strategy: Optional[str] = "",
        workload: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            cert_config(Dict[Any, Any]): certificate configuration

              FIELDS:
                ca	<Object>
                  CA configuration
                  CA certs are kept in the CA bundle as long as they are valid

                client	<Object>
                  Client configuration
                  Certs are rotated and discarded

                server	<Object>
                  Server configuration
                  Certs are rotated and discarded

            clone_strategy_override(str): Clone strategy override: should we use a host-assisted copy even if
              snapshots are available?

            config(Dict[Any, Any]): CDIConfig at CDI level

              FIELDS:
                dataVolumeTTLSeconds	<integer>
                  DataVolumeTTLSeconds is the time in seconds after DataVolume completion it
                  can be garbage collected. Disabled by default.

                featureGates	<[]string>
                  FeatureGates are a list of specific enabled feature gates

                filesystemOverhead	<Object>
                  FilesystemOverhead describes the space reserved for overhead when using
                  Filesystem volumes. A value is between 0 and 1, if not defined it is 0.055
                  (5.5% overhead)

                imagePullSecrets	<[]Object>
                  The imagePullSecrets used to pull the container images

                importProxy	<Object>
                  ImportProxy contains importer pod proxy configuration.

                insecureRegistries	<[]string>
                  InsecureRegistries is a list of TLS disabled registries

                logVerbosity	<integer>
                  LogVerbosity overrides the default verbosity level used to initialize
                  loggers

                podResourceRequirements	<Object>
                  ResourceRequirements describes the compute resource requirements.

                preallocation	<boolean>
                  Preallocation controls whether storage for DataVolumes should be allocated
                  in advance.

                scratchSpaceStorageClass	<string>
                  Override the storage class to used for scratch space during transfer
                  operations. The scratch space storage class is determined in the following
                  order: 1. value of scratchSpaceStorageClass, if that doesn't exist, use the
                  default storage class, if there is no default storage class, use the storage
                  class of the DataVolume, if no storage class specified, use no storage class
                  for scratch space

                tlsSecurityProfile	<Object>
                  TLSSecurityProfile is used by operators to apply cluster-wide TLS security
                  settings to operands.

                uploadProxyURLOverride	<string>
                  Override the URL used when uploading to a DataVolume

            customize_components(Dict[Any, Any]): CustomizeComponents defines patches for components deployed by the CDI
              operator.

              FIELDS:
                flags	<Object>
                  Configure the value used for deployment and daemonset resources

                patches	<[]Object>
                  <no description>

            image_pull_policy(str): PullPolicy describes a policy for if/when to pull a container image

            infra(Dict[Any, Any]): Selectors and tolerations that should apply to cdi infrastructure components

              FIELDS:
                affinity	<Object>
                  affinity enables pod affinity/anti-affinity placement expanding the types of
                  constraints
                  that can be expressed with nodeSelector.
                  affinity is going to be applied to the relevant kind of pods in parallel
                  with nodeSelector
                  See
                  https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity

                apiServerReplicas	<integer>
                  ApiserverReplicas set Replicas for cdi-apiserver

                deploymentReplicas	<integer>
                  DeploymentReplicas set Replicas for cdi-deployment

                nodeSelector	<map[string]string>
                  nodeSelector is the node selector applied to the relevant kind of pods
                  It specifies a map of key-value pairs: for the pod to be eligible to run on
                  a node,
                  the node must have each of the indicated key-value pairs as labels
                  (it can have additional labels as well).
                  See
                  https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#nodeselector

                tolerations	<[]Object>
                  tolerations is a list of tolerations applied to the relevant kind of pods
                  See https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/
                  for more info.
                  These are additional tolerations other than default ones.

                uploadProxyReplicas	<integer>
                  UploadproxyReplicas set Replicas for cdi-uploadproxy

            priority_class(str): PriorityClass of the CDI control plane

            uninstall_strategy(str): CDIUninstallStrategy defines the state to leave CDI on uninstall

            workload(Dict[Any, Any]): Restrict on which nodes CDI workload pods will be scheduled

              FIELDS:
                affinity	<Object>
                  affinity enables pod affinity/anti-affinity placement expanding the types of
                  constraints
                  that can be expressed with nodeSelector.
                  affinity is going to be applied to the relevant kind of pods in parallel
                  with nodeSelector
                  See
                  https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity

                nodeSelector	<map[string]string>
                  nodeSelector is the node selector applied to the relevant kind of pods
                  It specifies a map of key-value pairs: for the pod to be eligible to run on
                  a node,
                  the node must have each of the indicated key-value pairs as labels
                  (it can have additional labels as well).
                  See
                  https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#nodeselector

                tolerations	<[]Object>
                  tolerations is a list of tolerations applied to the relevant kind of pods
                  See https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/
                  for more info.
                  These are additional tolerations other than default ones.

        """
        super().__init__(**kwargs)

        self.cert_config = cert_config
        self.clone_strategy_override = clone_strategy_override
        self.config = config
        self.customize_components = customize_components
        self.image_pull_policy = image_pull_policy
        self.infra = infra
        self.priority_class = priority_class
        self.uninstall_strategy = uninstall_strategy
        self.workload = workload

    def to_dict(self) -> None:
        super().to_dict()

        if not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.cert_config:
                _spec["certConfig"] = self.cert_config

            if self.clone_strategy_override:
                _spec["cloneStrategyOverride"] = self.clone_strategy_override

            if self.config:
                _spec["config"] = self.config

            if self.customize_components:
                _spec["customizeComponents"] = self.customize_components

            if self.image_pull_policy:
                _spec["imagePullPolicy"] = self.image_pull_policy

            if self.infra:
                _spec["infra"] = self.infra

            if self.priority_class:
                _spec["priorityClass"] = self.priority_class

            if self.uninstall_strategy:
                _spec["uninstallStrategy"] = self.uninstall_strategy

            if self.workload:
                _spec["workload"] = self.workload
