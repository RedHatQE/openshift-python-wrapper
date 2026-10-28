import atexit
import os
import tempfile
from typing import Any

import kubernetes
import yaml
from kubernetes.dynamic import DynamicClient
from simple_logger.logger import get_logger

LOGGER = get_logger(name=__name__)


class DynamicClientWithKubeconfig(DynamicClient):
    def __init__(self, client: kubernetes.client.ApiClient, kubeconfig: str) -> None:
        super().__init__(client=client)
        self.kubeconfig = kubeconfig


def resolve_bearer_token(
    token: str | None,
    client_configuration: "kubernetes.client.Configuration",
) -> str | None:
    """Extract bearer token from client configuration if not explicitly provided."""
    if token:
        return token

    if client_configuration.api_key:
        _bearer = client_configuration.api_key.get("authorization", "")
        if _bearer.startswith("Bearer "):
            return _bearer.removeprefix("Bearer ")

    return None


def save_kubeconfig(
    host: str | None = None,
    token: str | None = None,
    config_dict: dict[str, Any] | None = None,
    verify_ssl: bool | None = None,
) -> str:
    """
    Save kubeconfig to a temporary file.

    Builds a kubeconfig from the provided parameters and writes it to a
    temporary file with 0o600 permissions.

    Args:
        host (str): cluster API server URL.
        token (str): bearer token for authentication.
        config_dict (dict): existing kubeconfig dict to save as-is.
        verify_ssl (bool): if False, sets insecure-skip-tls-verify in the saved config.

    Returns:
        str: path to the temporary kubeconfig file.
    """
    if config_dict is not None:
        _config = config_dict
    elif host:
        cluster_config: dict[str, Any] = {"server": host}
        if verify_ssl is False:
            cluster_config["insecure-skip-tls-verify"] = True

        user_config: dict[str, str] = {}
        if token:
            user_config["token"] = token

        _config = {
            "apiVersion": "v1",
            "kind": "Config",
            "clusters": [{"name": "cluster", "cluster": cluster_config}],
            "users": [{"name": "user", "user": user_config}],
            "contexts": [{"name": "context", "context": {"cluster": "cluster", "user": "user"}}],
            "current-context": "context",
        }
    else:
        raise ValueError("Not enough data to build kubeconfig: provide config_dict or host")

    fd = None
    tmp_path = None
    try:
        fd, tmp_path = tempfile.mkstemp(suffix=".kubeconfig")
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w") as f:
            fd = None
            yaml.safe_dump(_config, f)
        atexit.register(lambda p: os.unlink(p) if os.path.exists(p) else None, tmp_path)
        LOGGER.info(f"kubeconfig saved to {tmp_path}")
        return tmp_path

    except (OSError, yaml.YAMLError):
        if fd is not None:
            os.close(fd)
        if tmp_path is not None and os.path.exists(tmp_path):
            os.unlink(tmp_path)
        LOGGER.error("Failed to save kubeconfig")
        raise
