import os
import tempfile
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
    """
    Save kubeconfig to a file.

    Builds a kubeconfig from the provided parameters and writes it to the specified path.
    File is created with 0o600 permissions. Errors are logged but not raised.

    Args:
        path (str): path to save the kubeconfig file.
        host (str): cluster API server URL.
        token (str): bearer token for authentication.
        config_dict (dict): existing kubeconfig dict to save as-is.
        config_file (str): path to an existing kubeconfig file to copy.
        verify_ssl (bool): if False, sets insecure-skip-tls-verify in the saved config.
    """
    if config_dict is not None:
        _config = config_dict
    elif config_file:
        try:
            with open(config_file) as f:
                _config = yaml.safe_load(f)
        except (OSError, yaml.YAMLError):
            LOGGER.error(f"Failed to read config file {config_file}")
            raise
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
        raise ValueError("Not enough data to build kubeconfig: provide config_dict, config_file, or host")

    try:
        directory = os.path.dirname(os.path.abspath(path))
        os.makedirs(directory, exist_ok=True)

        fd, tmp_path = tempfile.mkstemp(dir=directory)
        try:
            os.fchmod(fd, 0o600)
            with os.fdopen(fd, "w") as f:
                yaml.safe_dump(_config, f)
            os.replace(tmp_path, path)
        except BaseException:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
            raise
    except (OSError, yaml.YAMLError):
        LOGGER.error(f"Failed to save kubeconfig to {path}")
        raise
