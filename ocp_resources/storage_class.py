# -*- coding: utf-8 -*-
from kubernetes.dynamic.exceptions import ResourceNotFoundError

from ocp_resources.resource import MissingRequiredArgumentError, Resource
from ocp_resources.storage_profile import StorageProfile


class StorageClass(Resource):
    """
    StorageClass object.
    """

    api_group = Resource.ApiGroup.STORAGE_K8S_IO

    class Types:
        """
        These are names of StorageClass instances when you run `oc get sc`

        API:
        https://kubernetes.io/docs/concepts/storage/storage-classes/
        """

        LOCAL_BLOCK = "local-block"
        HOSTPATH = "hostpath-provisioner"
        CEPH_RBD = "ocs-storagecluster-ceph-rbd"
        NFS = "nfs"
        HOSTPATH_CSI = "hostpath-csi"

    class Provisioner:
        HOSTPATH = "kubevirt.io/hostpath-provisioner"
        NO_PROVISIONER = "kubernetes.io/no-provisioner"
        CEPH_RBD = "openshift-storage.rbd.csi.ceph.com"
        HOSTPATH_CSI = "kubevirt.io.hostpath-provisioner"

    class VolumeBindingMode:
        """
        VolumeBindingMode indicates how PersistentVolumeClaims should be provisioned and bound.
        When unset, Immediate is used.
        When "Immediate", if you want to use the "node aware" hostpath-provisioner,
        ProvisionOnNode annotations should be introduced to PVC.
        Or in order to be able to use the hpp without specifying the node on the PVC,
        since CNV-2.2, hpp supports for "WaitForFirstConsumer".
        """

        # TODO: Rename to Uppercase
        Immediate = "Immediate"
        WaitForFirstConsumer = "WaitForFirstConsumer"

    class Annotations:
        IS_DEFAULT_CLASS = f"{Resource.ApiGroup.STORAGECLASS_KUBERNETES_IO}/is-default-class"
        IS_DEFAULT_VIRT_CLASS = f"{Resource.ApiGroup.STORAGECLASS_KUBEVIRT_IO}/is-default-virt-class"

    class ReclaimPolicy:
        DELETE = "Delete"
        RETAIN = "Retain"

    def __init__(
        self,
        provisioner=None,
        reclaim_policy=None,
        volume_binding_mode=None,
        allow_volume_expansion=None,
        parameters=None,
        allowed_topologies=None,
        mount_options=None,
        **kwargs,
    ):
        """
        StorageClass object

        Args:
            provisioner (str): The provisioner of the storage class
            reclaim_policy (str): Can be either "Delete" or "Retain"
            volume_binding_mode (str): When volume binding and dynamic provisioning should occur
            allow_volume_expansion (bool): True for allowing the volume expansion
            parameters (dict): Describe volumes belonging to the storage class.
            allowed_topologies (list): Restrict provisioning to specific topologies
            mount_options (list): PV's that are dynamically created by the SC will have the mount options
        """
        super().__init__(
            **kwargs,
        )

        self.provisioner = provisioner
        self.reclaim_policy = reclaim_policy
        self.volume_binding_mode = volume_binding_mode
        self.allow_volume_expansion = allow_volume_expansion
        self.parameters = parameters
        self.allowed_topologies = allowed_topologies
        self.mount_options = mount_options

    def to_dict(self) -> None:
        super().to_dict()
        if not self.yaml_file:
            if not self.provisioner:
                raise MissingRequiredArgumentError(argument="provisioner")
            self.res.update({"provisioner": self.provisioner})
            if self.reclaim_policy:
                self.res.update({"reclaimPolicy": self.reclaim_policy})
            if self.volume_binding_mode:
                self.res.update({"volumeBindingMode": self.volume_binding_mode})
            if self.allow_volume_expansion:
                self.res.update({"allowVolumeExpansion": self.allow_volume_expansion})
            if self.parameters:
                self.res.update({"parameters": self.parameters})
            if self.allowed_topologies:
                self.res.update({"allowedTopologies": self.allowed_topologies})
            if self.mount_options:
                self.res.update({"mountOptions": self.mount_options})

    @property
    def storage_profile(self):
        try:
            return StorageProfile(
                client=self.client,
                name=self.name,
            )
        except ResourceNotFoundError:
            self.logger.error(f" storageProfile is not found for {self.name}  storageClass")
            raise
