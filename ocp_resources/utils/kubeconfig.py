import os
from typing import Any

import yaml
from simple_logger.logger import get_logger

LOGGER = get_logger(name=__name__)


def save_kubeconfig(
    path: str,
    host: str | None = None,
    token: str | None = None,
    config_dict: dict[str, Any] | None = None,
    config_file: str | None = None,
    verify_ssl: bool | None = None,
) -> None:
    if config_dict:
        _config = config_dict
    elif config_file:
        with open(config_file) as f:
            _config = yaml.safe_load(f)
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
        LOGGER.warning("kubeconfig_output_path provided but not enough data to build kubeconfig")
        return

    try:
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        fd = os.open(path, os.O_CREAT | os.O_WRONLY | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w") as f:
            yaml.safe_dump(_config, f)
    except OSError:
        LOGGER.error(f"Failed to save kubeconfig to {path}", exc_info=True)
