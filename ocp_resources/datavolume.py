# -*- coding: utf-8 -*-

from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.persistent_volume_claim import PersistentVolumeClaim
from ocp_resources.resource import NamespacedResource, Resource
from ocp_resources.utils import TimeoutExpiredError, TimeoutSampler


class DataVolume(NamespacedResource):
    """
    DataVolume object.
    """

    api_group = NamespacedResource.ApiGroup.CDI_KUBEVIRT_IO

    class Status(NamespacedResource.Status):
        BLANK = "Blank"
        PVC_BOUND = "PVCBound"
        IMPORT_SCHEDULED = "ImportScheduled"
        ClONE_SCHEDULED = "CloneScheduled"
        UPLOAD_SCHEDULED = "UploadScheduled"
        IMPORT_IN_PROGRESS = "ImportInProgress"
        CLONE_IN_PROGRESS = "CloneInProgress"
        UPLOAD_IN_PROGRESS = "UploadInProgress"
        SNAPSHOT_FOR_SMART_CLONE_IN_PROGRESS = "SnapshotForSmartCloneInProgress"
        SMART_CLONE_PVC_IN_PROGRESS = "SmartClonePVCInProgress"
        UPLOAD_READY = "UploadReady"
        UNKNOWN = "Unknown"
        WAIT_FOR_FIRST_CONSUMER = "WaitForFirstConsumer"

    class AccessMode:
        """
        AccessMode object.
        """

        RWO = "ReadWriteOnce"
        ROX = "ReadOnlyMany"
        RWX = "ReadWriteMany"

    class ContentType:
        """
        ContentType object
        """

        KUBEVIRT = "kubevirt"
        ARCHIVE = "archive"

    class VolumeMode:
        """
        VolumeMode object
        """

        BLOCK = "Block"
        FILE = "Filesystem"

    class Condition:
        class Type:
            READY = "Ready"
            BOUND = "Bound"
            RUNNING = "Running"

        class Status(Resource.Condition.Status):
            UNKNOWN = "Unknown"

    def __init__(
        self,
        name=None,
        namespace=None,
        source=None,
        size=None,
        storage_class=None,
        url=None,
        content_type=ContentType.KUBEVIRT,
        access_modes=None,
        cert_configmap=None,
        secret=None,
        client=None,
        volume_mode=None,
        hostpath_node=None,
        source_pvc=None,
        source_namespace=None,
        multus_annotation=None,
        bind_immediate_annotation=None,
        preallocation=None,
        teardown=True,
        privileged_client=None,
        yaml_file=None,
        delete_timeout=TIMEOUT_4MINUTES,
        api_name="pvc",
        **kwargs,
    ):
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            teardown=teardown,
            privileged_client=privileged_client,
            yaml_file=yaml_file,
            delete_timeout=delete_timeout,
            **kwargs,
        )
        self.source = source
        self.url = url
        self.cert_configmap = cert_configmap
        self.secret = secret
        self.content_type = content_type
        self.size = size
        self.access_modes = access_modes
        self.storage_class = storage_class
        self.volume_mode = volume_mode
        self.hostpath_node = hostpath_node
        self.source_pvc = source_pvc
        self.source_namespace = source_namespace
        self.multus_annotation = multus_annotation
        self.bind_immediate_annotation = bind_immediate_annotation
        self.preallocation = preallocation
        self.api_name = api_name

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file:
            self.res.update(
                {
                    "spec": {
                        "source": {self.source: {"url": self.url}},
                        self.api_name: {
                            "resources": {"requests": {"storage": self.size}},
                        },
                    }
                }
            )
            if self.access_modes:
                self.res["spec"][self.api_name]["accessModes"] = [self.access_modes]
            if self.content_type:
                self.res["spec"]["contentType"] = self.content_type
            if self.storage_class:
                self.res["spec"][self.api_name]["storageClassName"] = self.storage_class
            if self.secret:
                self.res["spec"]["source"][self.source]["secretRef"] = self.secret.name
            if self.volume_mode:
                self.res["spec"][self.api_name]["volumeMode"] = self.volume_mode
            if self.source == "http" or "registry":
                self.res["spec"]["source"][self.source]["url"] = self.url
            if self.cert_configmap:
                self.res["spec"]["source"][self.source][
                    "certConfigMap"
                ] = self.cert_configmap
            if self.source == "upload" or self.source == "blank":
                self.res["spec"]["source"][self.source] = {}
            if self.hostpath_node:
                self.res["metadata"].setdefault("annotations", {}).update(
                    {
                        f"{NamespacedResource.ApiGroup.KUBEVIRT_IO}/provisionOnNode": self.hostpath_node
                    }
                )
            if self.multus_annotation:
                self.res["metadata"].setdefault("annotations", {}).update(
                    {
                        f"{NamespacedResource.ApiGroup.K8S_V1_CNI_CNCF_IO}/networks": self.multus_annotation
                    }
                )
            if self.bind_immediate_annotation:
                self.res["metadata"].setdefault("annotations", {}).update(
                    {
                        f"{NamespacedResource.ApiGroup.CDI_KUBEVIRT_IO}/storage.bind.immediate.requested": "true"
                    }
                )
            if self.source == "pvc":
                self.res["spec"]["source"]["pvc"] = {
                    "name": self.source_pvc or "dv-source",
                    "namespace": self.source_namespace or self.namespace,
                }
            if self.preallocation is not None:
                self.res["spec"]["preallocation"] = self.preallocation

    def wait_deleted(self, timeout=TIMEOUT_4MINUTES):
        """
        Wait until DataVolume and the PVC created by it are deleted

        Args:
        timeout (int):  Time to wait for the DataVolume and PVC to be deleted.

        Returns:
        bool: True if DataVolume and its PVC are gone, False if timeout reached.
        """
        super().wait_deleted(timeout=timeout)
        return self.pvc.wait_deleted(timeout=timeout)

    def wait(self, timeout=600, failure_timeout=120):
        self._check_none_pending_status(failure_timeout=failure_timeout)

        # If DV's status is not Pending, continue with the flow
        self.wait_for_status(status=self.Status.SUCCEEDED, timeout=timeout)
        self.pvc.wait_for_status(
            status=PersistentVolumeClaim.Status.BOUND, timeout=timeout
        )

    @property
    def pvc(self):
        return PersistentVolumeClaim(
            client=self.privileged_client or self.client,
            name=self.name,
            namespace=self.namespace,
        )

    @property
    def scratch_pvc(self):
        return PersistentVolumeClaim(
            name=f"{self.name}-scratch",
            namespace=self.namespace,
            client=self.client,
        )

    def _check_none_pending_status(self, failure_timeout=120):
        # Avoid waiting for "Succeeded" status if DV's in Pending/None status
        sample = None
        try:
            for sample in TimeoutSampler(
                wait_timeout=failure_timeout,
                sleep=10,
                func=lambda: self.instance.status.phase,
            ):
                # If DV status is Pending (or Status is not yet updated) continue to wait, else exit the wait loop
                if sample in [self.Status.PENDING, None]:
                    continue
                else:
                    break
        except TimeoutExpiredError:
            self.logger.error(f"{self.name} status is {sample}")
            raise
