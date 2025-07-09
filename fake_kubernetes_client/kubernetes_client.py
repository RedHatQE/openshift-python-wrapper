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
        path_params: Union[dict[str, Any], None] = None,
        query_params: Union[list[tuple[str, Any]], None] = None,
        header_params: Union[dict[str, Any], None] = None,
        body: Any = None,
        post_params: Union[list[tuple[str, Any]], None] = None,
        files: Union[dict[str, Any], None] = None,
        response_type: Union[str, None] = None,
        auth_settings: Union[list[str], None] = None,
        async_req: Union[bool, None] = None,
        _return_http_data_only: Union[bool, None] = None,
        collection_formats: Union[dict[str, Any], None] = None,
        _preload_content: Union[bool, None] = None,
        _request_timeout: Union[int, None] = None,
    ) -> Any:
        """
        Fake implementation of API calls.

        Currently only handles GET requests to "/api/v1" for API resource listing.
        All other requests return None.

        This is a minimal implementation sufficient for basic testing scenarios.
        """
        if self.dynamic_client and method == "GET" and "/api/v1" in resource_path:
            # Handle API resource listing
            if resource_path == "/api/v1":
                return FakeResourceField(data={"kind": "APIResourceList", "groupVersion": "v1", "resources": []})
        return None
