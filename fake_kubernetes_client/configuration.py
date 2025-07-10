"""FakeConfiguration implementation for fake Kubernetes client"""


class FakeConfiguration:
    """Fake implementation of kubernetes.client.Configuration"""

    def __init__(self) -> None:
        self.host = "https://fake-cluster.example.com:6443"
        self.api_key = {"authorization": "Bearer fake-token"}
        self.api_key_prefix = {"authorization": "Bearer"}
        self.username = None
        self.password = None
        self.verify_ssl = True
        self.ssl_ca_cert = None
        self.cert_file = None
        self.key_file = None
        self.assert_hostname = None
        self.connection_pool_maxsize = 4
        self.proxy = None
        self.proxy_headers = None
        self.safe_chars_for_path_param = ""
        self.retries = None
