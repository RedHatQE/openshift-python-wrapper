# -*- coding: utf-8 -*-


from .resource import NamespacedResource


class VirtualMachineRestore(NamespacedResource):
    """
    VirtualMachineRestore object.
    """

    api_group = NamespacedResource.ApiGroup.SNAPSHOT_KUBEVIRT_IO

    def __init__(self, name, namespace, vm_name, snapshot_name, teardown=True):
        super().__init__(name=name, namespace=namespace, teardown=teardown)
        self.vm_name = vm_name
        self.snapshot_name = snapshot_name

    def to_dict(self):
        res = super().to_dict()
        spec = res.setdefault("spec", {})
        spec.setdefault("target", {})[
            "apiGroup"
        ] = NamespacedResource.ApiGroup.KUBEVIRT_IO
        spec["target"]["kind"] = "VirtualMachine"
        spec["target"]["name"] = self.vm_name
        spec["virtualMachineSnapshotName"] = self.snapshot_name
        return res
