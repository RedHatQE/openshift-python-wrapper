"""FakeKubernetesClient implementation for fake Kubernetes client"""

from typing import TYPE_CHECKING, Any, Union

from fake_kubernetes_client.configuration import FakeConfiguration
from fake_kubernetes_client.resource_field import FakeResourceField

if TYPE_CHECKING:
    from fake_kubernetes_client.dynamic_client import FakeDynamicClient


class FakeKubernetesClient:
    """Fake implementation of kubernetes.client.ApiClient"""

    def __init__(
        self,
        configuration: Union[FakeConfiguration, None] = None,
        dynamic_client: Union["FakeDynamicClient", None] = None,
    ) -> None:
        self.configuration = configuration or FakeConfiguration()
        self.dynamic_client = dynamic_client

    def call_api(
        self,
        resource_path: str,
        method: str,
        path_params: dict[str, Any] | None = None,
        query_params: list[tuple[str, Any]] | None = None,
        header_params: dict[str, Any] | None = None,
        body: Any = None,
        post_params: list[tuple[str, Any]] | None = None,
        files: dict[str, Any] | None = None,
        response_type: str | None = None,
        auth_settings: list[str] | None = None,
        async_req: bool | None = None,
        _return_http_data_only: bool | None = None,
        collection_formats: dict[str, Any] | None = None,
        _preload_content: bool | None = None,
        _request_timeout: int | None = None,
    ) -> Any:
        """Fake implementation of API calls - delegates to dynamic client if available"""
        if self.dynamic_client and method == "GET" and "/api/v1" in resource_path:
            # Handle API resource listing
            if resource_path == "/api/v1":
                return FakeResourceField(data={"kind": "APIResourceList", "groupVersion": "v1", "resources": []})
        return None
