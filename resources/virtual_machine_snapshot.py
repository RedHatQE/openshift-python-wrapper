# -*- coding: utf-8 -*-


from .resource import NamespacedResource


class VirtualMachineSnapshot(NamespacedResource):
    """
    VirtualMachineSnapshot object.
    """

    api_group = NamespacedResource.ApiGroup.SNAPSHOT_KUBEVIRT_IO

    def __init__(self, name, namespace, vm_name, teardown=True):
        super().__init__(name=name, namespace=namespace, teardown=teardown)
        self.vm_name = vm_name

    def to_dict(self):
        res = super().to_dict()
        spec = res.setdefault("spec", {})
        spec.setdefault("source", {})[
            "apiGroup"
        ] = NamespacedResource.ApiGroup.KUBEVIRT_IO
        spec["source"]["kind"] = "VirtualMachine"
        spec["source"]["name"] = self.vm_name
        return res
