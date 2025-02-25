# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, List, Optional
from ocp_resources.resource import Resource


class Image(Resource):
    """
        Image is an immutable representation of a container image and metadata at a point in time. Images are named by taking a hash of their contents (metadata and content) and any change in format, content, or metadata results in a new name. The images resource is primarily for use by cluster administrators and integrations like the cluster image registry - end users instead access images via the imagestreamtags or imagestreamimages resources. While image metadata is stored in the API, any integration that implements the container image registry API must provide its own storage for the raw manifest data, image config, and layer contents.

    Compatibility level 1: Stable within a major release for a minimum of 12 months or 3 minor releases (whichever is longer).
    """

    api_group: str = Resource.ApiGroup.IMAGE_OPENSHIFT_IO

    def __init__(
        self,
        docker_image_config: Optional[str] = "",
        docker_image_layers: Optional[List[Any]] = None,
        docker_image_manifest: Optional[str] = "",
        docker_image_manifest_media_type: Optional[str] = "",
        docker_image_manifests: Optional[List[Any]] = None,
        docker_image_metadata: Optional[Dict[str, Any]] = None,
        docker_image_metadata_version: Optional[str] = "",
        docker_image_reference: Optional[str] = "",
        docker_image_signatures: Optional[List[Any]] = None,
        signatures: Optional[List[Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            docker_image_config (str): DockerImageConfig is a JSON blob that the runtime uses to set up the
              container. This is a part of manifest schema v2. Will not be set
              when the image represents a manifest list.

            docker_image_layers (List[Any]): DockerImageLayers represents the layers in the image. May not be set
              if the image does not define that data or if the image represents
              a manifest list.

            docker_image_manifest (str): DockerImageManifest is the raw JSON of the manifest

            docker_image_manifest_media_type (str): DockerImageManifestMediaType specifies the mediaType of manifest. This
              is a part of manifest schema v2.

            docker_image_manifests (List[Any]): DockerImageManifests holds information about sub-manifests when the
              image represents a manifest list. When this field is present, no
              DockerImageLayers should be specified.

            docker_image_metadata (Dict[str, Any]): RawExtension is used to hold extensions in external versions.  To use
              this, make a field which has RawExtension as its type in your
              external, versioned struct, and Object in your internal struct.
              You also need to register your various plugin types.  // Internal
              package:          type MyAPIObject struct {
              runtime.TypeMeta `json:",inline"`                 MyPlugin
              runtime.Object `json:"myPlugin"`         }          type PluginA
              struct {                 AOption string `json:"aOption"`         }
              // External package:          type MyAPIObject struct {
              runtime.TypeMeta `json:",inline"`                 MyPlugin
              runtime.RawExtension `json:"myPlugin"`         }          type
              PluginA struct {                 AOption string `json:"aOption"`
              }  // On the wire, the JSON will look something like this:
              {                 "kind":"MyAPIObject",
              "apiVersion":"v1",                 "myPlugin": {
              "kind":"PluginA",                         "aOption":"foo",
              },         }  So what happens? Decode first uses json or yaml to
              unmarshal the serialized data into your external MyAPIObject. That
              causes the raw JSON to be stored, but not unpacked. The next step
              is to copy (using pkg/conversion) into the internal struct. The
              runtime package's DefaultScheme has conversion functions installed
              which will unpack the JSON stored in RawExtension, turning it into
              the correct object type, and storing it in the Object. (TODO: In
              the case where the object is of an unknown type, a runtime.Unknown
              object will be created and stored.)

            docker_image_metadata_version (str): DockerImageMetadataVersion conveys the version of the object, which if
              empty defaults to "1.0"

            docker_image_reference (str): DockerImageReference is the string that can be used to pull this
              image.

            docker_image_signatures (List[Any]): DockerImageSignatures provides the signatures as opaque blobs. This is
              a part of manifest schema v1.

            signatures (List[Any]): Signatures holds all signatures of the image.

        """
        super().__init__(**kwargs)

        self.docker_image_config = docker_image_config
        self.docker_image_layers = docker_image_layers
        self.docker_image_manifest = docker_image_manifest
        self.docker_image_manifest_media_type = docker_image_manifest_media_type
        self.docker_image_manifests = docker_image_manifests
        self.docker_image_metadata = docker_image_metadata
        self.docker_image_metadata_version = docker_image_metadata_version
        self.docker_image_reference = docker_image_reference
        self.docker_image_signatures = docker_image_signatures
        self.signatures = signatures

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.docker_image_config:
                self.res["dockerImageConfig"] = self.docker_image_config

            if self.docker_image_layers:
                self.res["dockerImageLayers"] = self.docker_image_layers

            if self.docker_image_manifest:
                self.res["dockerImageManifest"] = self.docker_image_manifest

            if self.docker_image_manifest_media_type:
                self.res["dockerImageManifestMediaType"] = self.docker_image_manifest_media_type

            if self.docker_image_manifests:
                self.res["dockerImageManifests"] = self.docker_image_manifests

            if self.docker_image_metadata:
                self.res["dockerImageMetadata"] = self.docker_image_metadata

            if self.docker_image_metadata_version:
                self.res["dockerImageMetadataVersion"] = self.docker_image_metadata_version

            if self.docker_image_reference:
                self.res["dockerImageReference"] = self.docker_image_reference

            if self.docker_image_signatures:
                self.res["dockerImageSignatures"] = self.docker_image_signatures

            if self.signatures:
                self.res["signatures"] = self.signatures

    # End of generated code
