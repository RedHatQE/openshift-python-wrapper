# -*- coding: utf-8 -*-

from ocp_resources.resource import Resource


class StorageClass(Resource):
    """
    StorageClass object.
    """

    api_group = Resource.ApiGroup.STORAGE_K8S_IO

    class Types:
        """
        These are names of StorageClass instances when you run `oc get sc`
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
        IS_DEFAULT_CLASS = (
            f"{Resource.ApiGroup.STORAGECLASS_KUBERNETES_IO}/is-default-class"
        )
