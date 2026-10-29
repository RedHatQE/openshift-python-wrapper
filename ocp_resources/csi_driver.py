# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md


from typing import Any

from ocp_resources.resource import Resource


class CSIDriver(Resource):
    """
    CSIDriver captures information about a Container Storage Interface (CSI) volume driver deployed on the cluster. Kubernetes attach detach controller uses this object to determine whether attach is required. Kubelet uses this object to determine whether pod information needs to be passed on mount. CSIDriver objects are non-namespaced.
    """

    api_group: str = Resource.ApiGroup.STORAGE_K8S_IO

    def __init__(
        self,
        attach_required: bool | None = None,
        fs_group_policy: str | None = None,
        node_allocatable_update_period_seconds: int | None = None,
        pod_info_on_mount: bool | None = None,
        prevent_pod_scheduling_if_missing: bool | None = None,
        requires_republish: bool | None = None,
        se_linux_mount: bool | None = None,
        service_account_token_in_secrets: bool | None = None,
        storage_capacity: bool | None = None,
        token_requests: list[Any] | None = None,
        volume_lifecycle_modes: list[Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            attach_required (bool): attachRequired indicates this CSI volume driver requires an attach
              operation (because it implements the CSI ControllerPublishVolume()
              method), and that the Kubernetes attach detach controller should
              call the attach volume interface which checks the volumeattachment
              status and waits until the volume is attached before proceeding to
              mounting. The CSI external-attacher coordinates with CSI volume
              driver and updates the volumeattachment status when the attach
              operation is complete. If the value is specified to false, the
              attach operation will be skipped. Otherwise the attach operation
              will be called.  This field is immutable.

            fs_group_policy (str): fsGroupPolicy defines if the underlying volume supports changing
              ownership and permission of the volume before being mounted. Refer
              to the specific FSGroupPolicy values for additional details.  This
              field was immutable in Kubernetes < 1.29 and now is mutable.
              Defaults to ReadWriteOnceWithFSType, which will examine each
              volume to determine if Kubernetes should modify ownership and
              permissions of the volume. With the default policy the defined
              fsGroup will only be applied if a fstype is defined and the
              volume's access mode contains ReadWriteOnce.

            node_allocatable_update_period_seconds (int): nodeAllocatableUpdatePeriodSeconds specifies the interval between
              periodic updates of the CSINode allocatable capacity for this
              driver. When set, both periodic updates and updates triggered by
              capacity-related failures are enabled. If not set, no updates
              occur (neither periodic nor upon detecting capacity-related
              failures), and the allocatable.count remains static. The minimum
              allowed value for this field is 10 seconds.  This feature requires
              the MutableCSINodeAllocatableCount feature gate to be enabled.
              This field is mutable.

            pod_info_on_mount (bool): podInfoOnMount indicates this CSI volume driver requires additional
              pod information (like podName, podUID, etc.) during mount
              operations, if set to true. If set to false, pod information will
              not be passed on mount. Default is false.  The CSI driver
              specifies podInfoOnMount as part of driver deployment. If true,
              Kubelet will pass pod information as VolumeContext in the CSI
              NodePublishVolume() calls. The CSI driver is responsible for
              parsing and validating the information passed in as VolumeContext.
              The following VolumeContext will be passed if podInfoOnMount is
              set to true. This list might grow, but the prefix will be used.
              "csi.storage.k8s.io/pod.name": pod.Name
              "csi.storage.k8s.io/pod.namespace": pod.Namespace
              "csi.storage.k8s.io/pod.uid": string(pod.UID)
              "csi.storage.k8s.io/ephemeral": "true" if the volume is an
              ephemeral inline volume                                 defined by
              a CSIVolumeSource, otherwise "false"
              "csi.storage.k8s.io/ephemeral" is a new feature in Kubernetes
              1.16. It is only required for drivers which support both the
              "Persistent" and "Ephemeral" VolumeLifecycleMode. Other drivers
              can leave pod info disabled and/or ignore this field. As
              Kubernetes 1.15 doesn't support this field, drivers can only
              support one mode when deployed on such a cluster and the
              deployment determines which mode that is, for example via a
              command line parameter of the driver.  This field was immutable in
              Kubernetes < 1.29 and now is mutable.

            prevent_pod_scheduling_if_missing (bool): PreventPodSchedulingIfMissing indicates that the CSI driver wants to
              prevent pod scheduling if the CSI driver on the node is missing.
              Enabling this option will prevent the scheduler (or any other
              component which embeds default scheduler such as cluster-
              autoscaler) from scheduling pods to nodes where CSI driver is not
              installed.  For components(such as cluster-autoscaler) that embed
              the scheduler and run pod placement simulations using scheduler
              plugins, they MUST be aware of CSI driver registration information
              via CSINode object. They must create simulated CSINode objects in
              addition to Node objects during scheduling simulation, otherwise
              if PreventPodSchedulingIfMissing is enabled globally for CSIDriver
              object, any newly created node may be rejected by the scheduler
              because of missing CSI driver information from the node.  This is
              an alpha feature and requires the VolumeLimitScaling feature gate
              to be enabled. Default is "false".

            requires_republish (bool): requiresRepublish indicates the CSI driver wants `NodePublishVolume`
              being periodically called to reflect any possible change in the
              mounted volume. This field defaults to false.  Note: After a
              successful initial NodePublishVolume call, subsequent calls to
              NodePublishVolume should only update the contents of the volume.
              New mount points will not be seen by a running container.

            se_linux_mount (bool): seLinuxMount specifies if the CSI driver supports "-o context" mount
              option.  When "true", the CSI driver must ensure that all volumes
              provided by this CSI driver can be mounted separately with
              different `-o context` options. This is typical for storage
              backends that provide volumes as filesystems on block devices or
              as independent shared volumes. Kubernetes will call NodeStage /
              NodePublish with "-o context=xyz" mount option when mounting a
              ReadWriteOncePod volume used in Pod that has explicitly set
              SELinux context. In the future, it may be expanded to other volume
              AccessModes. In any case, Kubernetes will ensure that the volume
              is mounted only with a single SELinux context.  When "false",
              Kubernetes won't pass any special SELinux mount options to the
              driver. This is typical for volumes that represent subdirectories
              of a bigger shared filesystem.  Default is "false".

            service_account_token_in_secrets (bool): serviceAccountTokenInSecrets is an opt-in for CSI drivers to indicate
              that service account tokens should be passed via the Secrets field
              in NodePublishVolumeRequest instead of the VolumeContext field.
              The CSI specification provides a dedicated Secrets field for
              sensitive information like tokens, which is the appropriate
              mechanism for handling credentials. This addresses security
              concerns where sensitive tokens were being logged as part of
              volume context.  When "true", kubelet will pass the tokens only in
              the Secrets field with the key
              "csi.storage.k8s.io/serviceAccount.tokens". The CSI driver must be
              updated to read tokens from the Secrets field instead of
              VolumeContext.  When "false" or not set, kubelet will pass the
              tokens in VolumeContext with the key
              "csi.storage.k8s.io/serviceAccount.tokens" (existing behavior).
              This maintains backward compatibility with existing CSI drivers.
              This field can only be set when TokenRequests is configured. The
              API server will reject CSIDriver specs that set this field without
              TokenRequests.  Default behavior if unset is to pass tokens in the
              VolumeContext field.

            storage_capacity (bool): storageCapacity indicates that the CSI volume driver wants pod
              scheduling to consider the storage capacity that the driver
              deployment will report by creating CSIStorageCapacity objects with
              capacity information, if set to true.  The check can be enabled
              immediately when deploying a driver. In that case, provisioning
              new volumes with late binding will pause until the driver
              deployment has published some suitable CSIStorageCapacity object.
              Alternatively, the driver can be deployed with the field unset or
              false and it can be flipped later when storage capacity
              information has been published.  This field was immutable in
              Kubernetes <= 1.22 and now is mutable.

            token_requests (list[Any]): tokenRequests indicates the CSI driver needs pods' service account
              tokens it is mounting volume for to do necessary authentication.
              Kubelet will pass the tokens in VolumeContext in the CSI
              NodePublishVolume calls. The CSI driver should parse and validate
              the following VolumeContext:
              "csi.storage.k8s.io/serviceAccount.tokens": {   "<audience>": {
              "token": <token>,     "expirationTimestamp": <expiration timestamp
              in RFC3339>,   },   ... }  Note: Audience in each TokenRequest
              should be different and at most one token is empty string. To
              receive a new token after expiry, RequiresRepublish can be used to
              trigger NodePublishVolume periodically.

            volume_lifecycle_modes (list[Any]): volumeLifecycleModes defines what kind of volumes this CSI volume
              driver supports. The default if the list is empty is "Persistent",
              which is the usage defined by the CSI specification and
              implemented in Kubernetes via the usual PV/PVC mechanism.  The
              other mode is "Ephemeral". In this mode, volumes are defined
              inline inside the pod spec with CSIVolumeSource and their
              lifecycle is tied to the lifecycle of that pod. A driver has to be
              aware of this because it is only going to get a NodePublishVolume
              call for such a volume.  For more information about implementing
              this mode, see https://kubernetes-csi.github.io/docs/ephemeral-
              local-volumes.html A driver can support one or more of these modes
              and more modes may be added in the future.  This field is beta.
              This field is immutable.

        """
        super().__init__(**kwargs)

        self.attach_required = attach_required
        self.fs_group_policy = fs_group_policy
        self.node_allocatable_update_period_seconds = node_allocatable_update_period_seconds
        self.pod_info_on_mount = pod_info_on_mount
        self.prevent_pod_scheduling_if_missing = prevent_pod_scheduling_if_missing
        self.requires_republish = requires_republish
        self.se_linux_mount = se_linux_mount
        self.service_account_token_in_secrets = service_account_token_in_secrets
        self.storage_capacity = storage_capacity
        self.token_requests = token_requests
        self.volume_lifecycle_modes = volume_lifecycle_modes

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.attach_required is not None:
                _spec["attachRequired"] = self.attach_required

            if self.fs_group_policy is not None:
                _spec["fsGroupPolicy"] = self.fs_group_policy

            if self.node_allocatable_update_period_seconds is not None:
                _spec["nodeAllocatableUpdatePeriodSeconds"] = self.node_allocatable_update_period_seconds

            if self.pod_info_on_mount is not None:
                _spec["podInfoOnMount"] = self.pod_info_on_mount

            if self.prevent_pod_scheduling_if_missing is not None:
                _spec["preventPodSchedulingIfMissing"] = self.prevent_pod_scheduling_if_missing

            if self.requires_republish is not None:
                _spec["requiresRepublish"] = self.requires_republish

            if self.se_linux_mount is not None:
                _spec["seLinuxMount"] = self.se_linux_mount

            if self.service_account_token_in_secrets is not None:
                _spec["serviceAccountTokenInSecrets"] = self.service_account_token_in_secrets

            if self.storage_capacity is not None:
                _spec["storageCapacity"] = self.storage_capacity

            if self.token_requests is not None:
                _spec["tokenRequests"] = self.token_requests

            if self.volume_lifecycle_modes is not None:
                _spec["volumeLifecycleModes"] = self.volume_lifecycle_modes

    # End of generated code
