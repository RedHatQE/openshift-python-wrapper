# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, List, Optional
from ocp_resources.resource import Resource


class CSIDriver(Resource):
    """
    CSIDriver captures information about a Container Storage Interface (CSI) volume driver deployed on the cluster. Kubernetes attach detach controller uses this object to determine whether attach is required. Kubelet uses this object to determine whether pod information needs to be passed on mount. CSIDriver objects are non-namespaced.
    """

    api_group: str = Resource.ApiGroup.STORAGE_K8S_IO

    def __init__(
        self,
        attach_required: Optional[bool] = None,
        fs_group_policy: Optional[str] = "",
        pod_info_on_mount: Optional[bool] = None,
        requires_republish: Optional[bool] = None,
        se_linux_mount: Optional[bool] = None,
        storage_capacity: Optional[bool] = None,
        token_requests: Optional[List[Any]] = None,
        volume_lifecycle_modes: Optional[List[Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            attach_required (bool): attachRequired indicates this CSI volume driver requires an attach
              operation (because it implements the CSI ControllerPublishVolume()
              method), and that the Kubernetes attach detach controller should
              call the attach volume interface which checks the volumeattachment
              status and waits until the volume is attached before proceeding to
              mounting. The CSI external-attacher coordinates with CSI volume
              driver and updates the volumeattachment status when the attach
              operation is complete. If the CSIDriverRegistry feature gate is
              enabled and the value is specified to false, the attach operation
              will be skipped. Otherwise the attach operation will be called.
              This field is immutable.

            fs_group_policy (str): fsGroupPolicy defines if the underlying volume supports changing
              ownership and permission of the volume before being mounted. Refer
              to the specific FSGroupPolicy values for additional details.  This
              field was immutable in Kubernetes < 1.29 and now is mutable.
              Defaults to ReadWriteOnceWithFSType, which will examine each
              volume to determine if Kubernetes should modify ownership and
              permissions of the volume. With the default policy the defined
              fsGroup will only be applied if a fstype is defined and the
              volume's access mode contains ReadWriteOnce.

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

            token_requests (List[Any]): tokenRequests indicates the CSI driver needs pods' service account
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

            volume_lifecycle_modes (List[Any]): volumeLifecycleModes defines what kind of volumes this CSI volume
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
        self.pod_info_on_mount = pod_info_on_mount
        self.requires_republish = requires_republish
        self.se_linux_mount = se_linux_mount
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

            if self.fs_group_policy:
                _spec["fsGroupPolicy"] = self.fs_group_policy

            if self.pod_info_on_mount is not None:
                _spec["podInfoOnMount"] = self.pod_info_on_mount

            if self.requires_republish is not None:
                _spec["requiresRepublish"] = self.requires_republish

            if self.se_linux_mount is not None:
                _spec["seLinuxMount"] = self.se_linux_mount

            if self.storage_capacity is not None:
                _spec["storageCapacity"] = self.storage_capacity

            if self.token_requests:
                _spec["tokenRequests"] = self.token_requests

            if self.volume_lifecycle_modes:
                _spec["volumeLifecycleModes"] = self.volume_lifecycle_modes

    # End of generated code
