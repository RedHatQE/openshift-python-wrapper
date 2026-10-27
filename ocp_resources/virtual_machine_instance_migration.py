# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md


from typing import Any

from ocp_resources.resource import NamespacedResource


class VirtualMachineInstanceMigration(NamespacedResource):
    """
        VirtualMachineInstanceMigration represents the object tracking a VMI's migration
    to another host in the cluster
    """

    api_group: str = NamespacedResource.ApiGroup.KUBEVIRT_IO

    def __init__(
        self,
        added_node_selector: dict[str, Any] | None = None,
        priority: str | None = None,
        receive: dict[str, Any] | None = None,
        send_to: dict[str, Any] | None = None,
        vmi_name: str | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            added_node_selector (dict[str, Any]): AddedNodeSelector is an additional selector that can be used to
              complement a NodeSelector or NodeAffinity as set on the VM to
              restrict the set of allowed target nodes for a migration. In case
              of key collisions, values set on the VM objects are going to be
              preserved to ensure that addedNodeSelector can only restrict but
              not bypass constraints already set on the VM object.

            priority (str): Priority of the migration. This can be one of 'system-critical',
              'user-triggered', 'system-maintenance'.

            receive (dict[str, Any]): If receieve is specified, this VirtualMachineInstanceMigration will be
              considered the target

            send_to (dict[str, Any]): If sendTo is specified, this VirtualMachineInstanceMigration will be
              considered the source

            vmi_name (str): The name of the VMI to perform the migration on. VMI must exist in the
              migration objects namespace

        """
        super().__init__(**kwargs)

        self.added_node_selector = added_node_selector
        self.priority = priority
        self.receive = receive
        self.send_to = send_to
        self.vmi_name = vmi_name

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.added_node_selector is not None:
                _spec["addedNodeSelector"] = self.added_node_selector

            if self.priority is not None:
                _spec["priority"] = self.priority

            if self.receive is not None:
                _spec["receive"] = self.receive

            if self.send_to is not None:
                _spec["sendTo"] = self.send_to

            if self.vmi_name is not None:
                _spec["vmiName"] = self.vmi_name

    # End of generated code
