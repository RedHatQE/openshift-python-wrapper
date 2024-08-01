# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, Optional
from ocp_resources.resource import Resource


class Image(Resource):
    """
    Image is an immutable representation of a container image and metadata at a
    point in time. Images are named by taking a hash of their contents (metadata
    and content) and any change in format, content, or metadata results in a new
    name. The images resource is primarily for use by cluster administrators and
    integrations like the cluster image registry - end users instead access
    images via the imagestreamtags or imagestreamimages resources. While image
    metadata is stored in the API, any integration that implements the container
    image registry API must provide its own storage for the raw manifest data,
    image config, and layer contents.
    """

    api_group: str = Resource.ApiGroup.IMAGE_OPENSHIFT_IO

    def __init__(
        self,
        docker_image_config: Optional[str] = "",
        docker_image_layers: Optional[Dict[str, Any]] = None,
        docker_image_manifest: Optional[str] = "",
        docker_image_manifest_media_type: Optional[str] = "",
        docker_image_manifests: Optional[Dict[str, Any]] = None,
        docker_image_metadata: Optional[Dict[str, Any]] = None,
        docker_image_metadata_version: Optional[str] = "",
        docker_image_reference: Optional[str] = "",
        docker_image_signatures: Optional[Dict[str, Any]] = None,
        signatures: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            docker_image_config(str): DockerImageConfig is a JSON blob that the runtime uses to set up the
              container. This is a part of manifest schema v2. Will not be set when the
              image represents a manifest list.

            docker_image_layers(Dict[Any, Any]): DockerImageLayers represents the layers in the image. May not be set if the
              image does not define that data or if the image represents a manifest list.
              ImageLayer represents a single layer of the image. Some images may have
              multiple layers. Some may have none.

              FIELDS:
                mediaType	<string> -required-
                  MediaType of the referenced object.

                name	<string> -required-
                  Name of the layer as defined by the underlying store.

                size	<integer> -required-
                  Size of the layer in bytes as defined by the underlying store.

            docker_image_manifest(str): DockerImageManifest is the raw JSON of the manifest

            docker_image_manifest_media_type(str): DockerImageManifestMediaType specifies the mediaType of manifest. This is a
              part of manifest schema v2.

            docker_image_manifests(Dict[Any, Any]): DockerImageManifests holds information about sub-manifests when the image
              represents a manifest list. When this field is present, no DockerImageLayers
              should be specified.
              ImageManifest represents sub-manifests of a manifest list. The Digest field
              points to a regular Image object.

              FIELDS:
                architecture	<string> -required-
                  Architecture specifies the supported CPU architecture, for example `amd64`
                  or `ppc64le`.

                digest	<string> -required-
                  Digest is the unique identifier for the manifest. It refers to an Image
                  object.

                manifestSize	<integer> -required-
                  ManifestSize represents the size of the raw object contents, in bytes.

                mediaType	<string> -required-
                  MediaType defines the type of the manifest, possible values are
                  application/vnd.oci.image.manifest.v1+json,
                  application/vnd.docker.distribution.manifest.v2+json or
                  application/vnd.docker.distribution.manifest.v1+json.

                os	<string> -required-
                  OS specifies the operating system, for example `linux`.

                variant	<string>
                  Variant is an optional field repreenting a variant of the CPU, for example
                  v6 to specify a particular CPU variant of the ARM CPU.

            docker_image_metadata(Dict[Any, Any]): DockerImageMetadata contains metadata about this image
              RawExtension is used to hold extensions in external versions.

              To use this, make a field which has RawExtension as its type in your
              external, versioned struct, and Object in your internal struct. You also
              need to register your various plugin types.

              // Internal package:

                type MyAPIObject struct {
                        runtime.TypeMeta `json:",inline"`
                        MyPlugin runtime.Object `json:"myPlugin"`
                }

                type PluginA struct {
                        AOption string `json:"aOption"`
                }

              // External package:

                type MyAPIObject struct {
                        runtime.TypeMeta `json:",inline"`
                        MyPlugin runtime.RawExtension `json:"myPlugin"`
                }

                type PluginA struct {
                        AOption string `json:"aOption"`
                }

              // On the wire, the JSON will look something like this:

                {
                        "kind":"MyAPIObject",
                        "apiVersion":"v1",
                        "myPlugin": {
                                "kind":"PluginA",
                                "aOption":"foo",
                        },
                }

              So what happens? Decode first uses json or yaml to unmarshal the serialized
              data into your external MyAPIObject. That causes the raw JSON to be stored,
              but not unpacked. The next step is to copy (using pkg/conversion) into the
              internal struct. The runtime package's DefaultScheme has conversion
              functions installed which will unpack the JSON stored in RawExtension,
              turning it into the correct object type, and storing it in the Object.
              (TODO: In the case where the object is of an unknown type, a runtime.Unknown
              object will be created and stored.)

            docker_image_metadata_version(str): DockerImageMetadataVersion conveys the version of the object, which if empty
              defaults to "1.0"

            docker_image_reference(str): DockerImageReference is the string that can be used to pull this image.

            docker_image_signatures(Dict[Any, Any]): DockerImageSignatures provides the signatures as opaque blobs. This is a
              part of manifest schema v1.

            signatures(Dict[Any, Any]): Signatures holds all signatures of the image.
              ImageSignature holds a signature of an image. It allows to verify image
              identity and possibly other claims as long as the signature is trusted.
              Based on this information it is possible to restrict runnable images to
              those matching cluster-wide policy. Mandatory fields should be parsed by
              clients doing image verification. The others are parsed from signature's
              content by the server. They serve just an informative purpose.

              Compatibility level 1: Stable within a major release for a minimum of 12
              months or 3 minor releases (whichever is longer).

              FIELDS:
                apiVersion	<string>
                  APIVersion defines the versioned schema of this representation of an object.
                  Servers should convert recognized schemas to the latest internal value, and
                  may reject unrecognized values. More info:
                  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources

                conditions	<[]SignatureCondition>
                  Conditions represent the latest available observations of a signature's
                  current state.

                content	<string> -required-
                  Required: An opaque binary string which is an image's signature.

                created	<string>
                  If specified, it is the time of signature's creation.

                imageIdentity	<string>
                  A human readable string representing image's identity. It could be a product
                  name and version, or an image pull spec (e.g.
                  "registry.access.redhat.com/rhel7/rhel:7.2").

                issuedBy	<SignatureIssuer>
                  If specified, it holds information about an issuer of signing certificate or
                  key (a person or entity who signed the signing certificate or key).

                issuedTo	<SignatureSubject>
                  If specified, it holds information about a subject of signing certificate or
                  key (a person or entity who signed the image).

                kind	<string>
                  Kind is a string value representing the REST resource this object
                  represents. Servers may infer this from the endpoint the client submits
                  requests to. Cannot be updated. In CamelCase. More info:
                  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds

                metadata	<ObjectMeta>
                  metadata is the standard object's metadata. More info:
                  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

                signedClaims	<map[string]string>
                  Contains claims from the signature.

                type	<string> -required-
                  Required: Describes a type of stored blob.

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

        if not self.yaml_file:
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
