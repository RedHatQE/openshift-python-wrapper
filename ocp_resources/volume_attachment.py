# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md


from typing import Any

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.resource import Resource


class VolumeAttachment(Resource):
    """
        VolumeAttachment captures the intent to attach or detach the specified volume to/from the specified node.

    VolumeAttachment objects are non-namespaced.
    """

    api_group: str = Resource.ApiGroup.STORAGE_K8S_IO

    def __init__(
        self,
        attacher: str | None = None,
        node_name: str | None = None,
        source: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            attacher (str): attacher indicates the name of the volume driver that MUST handle this
              request. This is the name returned by GetPluginName().

            node_name (str): nodeName represents the node that the volume should be attached to.

            source (dict[str, Any]): VolumeAttachmentSource represents a volume that should be attached.
              Right now only PersistentVolumes can be attached via external
              attacher, in the future we may allow also inline volumes in pods.
              Exactly one member can be set.

        """
        super().__init__(**kwargs)

        self.attacher = attacher
        self.node_name = node_name
        self.source = source

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.attacher is None:
                raise MissingRequiredArgumentError(argument="self.attacher")

            if self.node_name is None:
                raise MissingRequiredArgumentError(argument="self.node_name")

            if self.source is None:
                raise MissingRequiredArgumentError(argument="self.source")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["attacher"] = self.attacher
            _spec["nodeName"] = self.node_name
            _spec["source"] = self.source

    # End of generated code
