from ocp_resources.resource import NamespacedResource


class ServingRuntime(NamespacedResource):
    """
    ServingRuntime object
    """

    api_group = NamespacedResource.ApiGroup.SERVING_KSERVE_IO

    def __init__(
        self,
        supported_model_formats=None,
        protocol_versions=None,
        multi_model=None,
        containers=None,
        grpc_endpoint=None,
        grpc_data_endpoint=None,
        server_type=None,
        runtime_mgmt_port=None,
        mem_buffer_bytes=None,
        model_loading_timeout_millis=None,
        enable_route=None,
        **kwargs,
    ):
        """
        ServingRuntime object

        Args:
            supported_model_formats (List(dict)): Model formats supported by the serving runtime.
            protocol_versions (List(str)): List of protocols versions used by the serving runtime.
            multi_model (bool): Specifies if the model server can serve multiple models.
            containers (List(dict)): Containers of the serving runtime.
            grpc_endpoint (int): Port of the gRPC endpoint.
            grpc_data_endpoint (int): Port of the gRPC data endpoint.
            server_type (str): Type of the model server.
            runtime_mgmt_port (int): Runtime management port for the model server.
            mem_buffer_bytes (int): Memory buffer bytes.
            model_loading_timeout_millis (int): Model loading timeout in milliseconds
            enable_route (bool): Determines if a route is enabled for the model server.
        """
        super().__init__(**kwargs)
        self.supported_model_formats = supported_model_formats
        self.protocol_versions = (protocol_versions,)
        self.multi_model = (multi_model,)
        self.containers = containers
        self.grpc_endpoint = grpc_endpoint
        self.grpc_data_endpoint = grpc_data_endpoint
        self.server_type = server_type
        self.runtime_mgmt_port = runtime_mgmt_port
        self.mem_buffer_bytes = mem_buffer_bytes
        self.model_loading_timeout_millis = model_loading_timeout_millis
        self.enable_route = enable_route

    def to_dict(self):
        super().to_dict()

        self.res["spec"] = {}
        _spec = self.res["spec"]

        if self.enable_route:
            self.res["metadata"]["annotations"] = {"enable-route": "true"}

        if self.supported_model_formats:
            _spec["supportedModelFormats"] = self.supported_model_formats

        if self.protocol_versions:
            _spec["protocolVersions"] = self.protocol_versions

        if self.multi_model:
            _spec["multiModel"] = True

        if self.grpc_endpoint:
            _spec["grpcEndpoint"] = f"port:{self.grpc_endpoint}"

        if self.grpc_data_endpoint:
            _spec["grpcDataEndpoint"] = f"port:{self.grpc_data_endpoint}"

        if self.containers:
            _spec["containers"] = self.containers

        if self.server_type:
            _spec.setdefault("builtInAdapter", {})["serverType"] = self.server_type

        if self.runtime_mgmt_port:
            _spec.setdefault("builtInAdapter", {})["runtimeManagementPort"] = self.runtime_mgmt_port

        if self.mem_buffer_bytes:
            _spec.setdefault("builtInAdapter", {})["memBufferBytes"] = self.mem_buffer_bytes

        if self.model_loading_timeout_millis:
            _spec.setdefault("builtInAdapter", {})["modelLoadingTimeoutMillis"] = self.model_loading_timeout_millis
