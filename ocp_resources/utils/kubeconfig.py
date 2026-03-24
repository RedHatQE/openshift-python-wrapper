import atexit
import os
import tempfile
from typing import Any

import yaml
from simple_logger.logger import get_logger

LOGGER = get_logger(name=__name__)


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

    tmp_file = None
    try:
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".kubeconfig", mode="w")
        os.chmod(tmp_file.name, 0o600)
        yaml.safe_dump(_config, tmp_file)
        tmp_file.close()
        # Ensures the file is cleaned up when the process exits.
        atexit.register(lambda p: os.unlink(p) if os.path.exists(p) else None, tmp_file.name)
        LOGGER.info(f"kubeconfig saved to {tmp_file.name}")
        return tmp_file.name

    except (OSError, yaml.YAMLError):
        if tmp_file is not None and os.path.exists(tmp_file.name):
            os.unlink(tmp_file.name)
        LOGGER.error("Failed to save kubeconfig")
        raise
