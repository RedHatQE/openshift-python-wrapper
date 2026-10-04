# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md


from typing import Any

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.resource import NamespacedResource


class MCPServer(NamespacedResource):
    """
        MCPServer runs a Model Context Protocol (MCP) server in Kubernetes.

    MCPServer creates and manages a Deployment, Service, and NetworkPolicy to run an MCP server from a
    container image. The MCP server exposes tools, resources, and prompts that AI applications
    can use via the Model Context Protocol.

    Example:

            apiVersion: mcp.x-k8s.io/v1alpha1
            kind: MCPServer
            metadata:
              name: example
            spec:
              source:
                type: ContainerImage
                containerImage:
                  ref: example-mcp-image
              config:
                port: 8080

    The controller manages Deployment, Service, and NetworkPolicy resources with the same name as the MCPServer,
    using ownerReferences to establish ownership. The controller will reject updates to resources
    owned by other controllers or resources with no controller owner (to prevent silent overwrites
    of manually-created resources), but will adopt orphaned resources from a deleted MCPServer
    with the same name to enable seamless recreation.
    """

    api_group: str = NamespacedResource.ApiGroup.MCP_X_K8S_IO

    def __init__(
        self,
        config: dict[str, Any] | None = None,
        extra_annotations: dict[str, Any] | None = None,
        extra_labels: dict[str, Any] | None = None,
        mcp: dict[str, Any] | None = None,
        runtime: dict[str, Any] | None = None,
        source: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            config (dict[str, Any]): Config is a required field that defines how the MCP server should be
              configured when it runs. This includes runtime settings such as
              the server port, command-line arguments, environment variables,
              and storage mounts.

            extra_annotations (dict[str, Any]): ExtraAnnotations are applied to the Deployment metadata, PodTemplate
              metadata, and Service metadata.

            extra_labels (dict[str, Any]): ExtraLabels are applied to the Deployment metadata, PodTemplate
              metadata, and Service metadata. The operator-managed keys "app"
              and "mcp-server" cannot be overridden.

            mcp (dict[str, Any]): MCP defines Model Context Protocol specific properties of the server.
              This section describes the MCP server's protocol-level behavior,
              as opposed to how it is sourced, configured, or managed at
              runtime.

            runtime (dict[str, Any]): Runtime defines runtime management configuration. If not specified,
              default runtime settings will be applied.

            source (dict[str, Any]): Source is a required field that defines where the MCP server should be
              sourced from. Currently supports container images, with potential
              for additional source types in the future. This configuration
              determines how the MCP server will be deployed and run.

        """
        super().__init__(**kwargs)

        self.config = config
        self.extra_annotations = extra_annotations
        self.extra_labels = extra_labels
        self.mcp = mcp
        self.runtime = runtime
        self.source = source

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.config is None:
                raise MissingRequiredArgumentError(argument="self.config")

            if self.source is None:
                raise MissingRequiredArgumentError(argument="self.source")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["config"] = self.config
            _spec["source"] = self.source

            if self.extra_annotations is not None:
                _spec["extraAnnotations"] = self.extra_annotations

            if self.extra_labels is not None:
                _spec["extraLabels"] = self.extra_labels

            if self.mcp is not None:
                _spec["mcp"] = self.mcp

            if self.runtime is not None:
                _spec["runtime"] = self.runtime

    # End of generated code
