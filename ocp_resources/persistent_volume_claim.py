# -*- coding: utf-8 -*-

import logging

from ocp_resources.resource import NamespacedResource


LOGGER = logging.getLogger(__name__)


class PersistentVolumeClaim(NamespacedResource):
    """
    PersistentVolumeClaim object
    """

    api_version = NamespacedResource.ApiVersion.V1

    class Status(NamespacedResource.Status):
        BOUND = "Bound"
        TERMINATING = "Terminating"

    class AccessMode:
        """
        AccessMode object.
        """

        RWO = "ReadWriteOnce"
        ROX = "ReadOnlyMany"
        RWX = "ReadWriteMany"

    class VolumeMode:
        """
        VolumeMode object
        """

        BLOCK = "Block"
        FILE = "Filesystem"

    def __init__(
        self,
        name,
        namespace,
        client=None,
        storage_class=None,
        accessmodes=None,
        volume_mode=VolumeMode.FILE,
        size=None,
        hostpath_node=None,
        teardown=True,
    ):
        super().__init__(
            name=name, namespace=namespace, client=client, teardown=teardown
        )
        self.accessmodes = accessmodes
        self.volume_mode = volume_mode
        self.size = size
        self.hostpath_node = hostpath_node
        self.storage_class = storage_class

    def to_dict(self):
        res = super().to_dict()
        res.update(
            {
                "spec": {
                    "volumeMode": self.volume_mode,
                    "accessModes": [self.accessmodes],
                    "resources": {"requests": {"storage": self.size}},
                }
            }
        )
        """
        Hostpath-provisioner is "node aware", when using it,
        a node attribute on the claim must be introduced as follows.
        annotations:
          kubevirt.io/provisionOnNode: <specified_node_name>
        """
        if self.hostpath_node:
            res["metadata"]["annotations"] = {
                "kubevirt.io/provisionOnNode": self.hostpath_node
            }
        if self.storage_class:
            res["spec"]["storageClassName"] = self.storage_class

        return res

    def bound(self):
        """
        Check if PVC is bound

        Returns:
            bool: True if bound else False
        """
        LOGGER.info(f"Check if {self.kind} {self.name} is bound")
        return self.status == self.Status.BOUND

    @property
    def selected_node(self):
        return self.instance.metadata.annotations.get(
            "volume.kubernetes.io/selected-node"
        )
