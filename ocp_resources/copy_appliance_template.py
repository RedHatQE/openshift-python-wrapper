# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md


from typing import Any

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.resource import NamespacedResource


class CopyApplianceTemplate(NamespacedResource):
    """
    No field description from API
    """

    api_group: str = NamespacedResource.ApiGroup.FORKLIFT_KONVEYOR_IO

    def __init__(
        self,
        base_disk: dict[str, Any] | None = None,
        builder_image: str | None = None,
        datastore: str | None = None,
        folder: str | None = None,
        network: str | None = None,
        node_selector: dict[str, Any] | None = None,
        provider: dict[str, Any] | None = None,
        resources: dict[str, Any] | None = None,
        template_name: str | None = None,
        transfer_network: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            base_disk (dict[str, Any]): Base containerdisk image for overlay customization.

            builder_image (str): Override for the copy appliance template builder container image.
              Defaults to the controller COPY_APPLIANCE_TEMPLATE_BUILDER_IMAGE
              setting when empty.

            datastore (str): Target vCenter datastore.

            folder (str): vCenter folder path (e.g. /Datacenter/vm).

            network (str): Port group for OVF network mapping.

            node_selector (dict[str, Any]): Optional node selector for the build pod.

            provider (dict[str, Any]): Reference to a vSphere Provider.

            resources (dict[str, Any]): OVF hardware descriptor overrides.

            template_name (str): vCenter template name after OVF import.

            transfer_network (dict[str, Any]): Multus NAD for the OVA build pod (same as Plan.spec.transferNetwork).

        """
        super().__init__(**kwargs)

        self.base_disk = base_disk
        self.builder_image = builder_image
        self.datastore = datastore
        self.folder = folder
        self.network = network
        self.spec_node_selector = node_selector
        self.provider = provider
        self.resources = resources
        self.template_name = template_name
        self.transfer_network = transfer_network

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.base_disk is None:
                raise MissingRequiredArgumentError(argument="self.base_disk")

            if self.datastore is None:
                raise MissingRequiredArgumentError(argument="self.datastore")

            if self.folder is None:
                raise MissingRequiredArgumentError(argument="self.folder")

            if self.network is None:
                raise MissingRequiredArgumentError(argument="self.network")

            if self.provider is None:
                raise MissingRequiredArgumentError(argument="self.provider")

            if self.template_name is None:
                raise MissingRequiredArgumentError(argument="self.template_name")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["baseDisk"] = self.base_disk
            _spec["datastore"] = self.datastore
            _spec["folder"] = self.folder
            _spec["network"] = self.network
            _spec["provider"] = self.provider
            _spec["templateName"] = self.template_name

            if self.builder_image is not None:
                _spec["builderImage"] = self.builder_image

            if self.spec_node_selector is not None:
                _spec["nodeSelector"] = self.spec_node_selector

            if self.resources is not None:
                _spec["resources"] = self.resources

            if self.transfer_network is not None:
                _spec["transferNetwork"] = self.transfer_network

    # End of generated code
