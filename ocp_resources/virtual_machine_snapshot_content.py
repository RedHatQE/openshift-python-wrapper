from ocp_resources.resource import NamespacedResource


class VirtualMachineSnapshotContent(NamespacedResource):
    """
    VirtualMachineSnapshotContent object. API reference:
    https://docs.openshift.com/container-platform/4.11/virt/virtual_machines/virtual_disks/virt-managing-vm-snapshots.html
    """

    api_group = NamespacedResource.ApiGroup.SNAPSHOT_KUBEVIRT_IO
