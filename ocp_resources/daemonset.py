"""Backward-compatibility shim — use ``ocp_resources.daemon_set`` instead."""

import warnings

warnings.warn(
    "ocp_resources.daemonset is deprecated, use ocp_resources.daemon_set instead",
    DeprecationWarning,
    stacklevel=2,
)

from ocp_resources.daemon_set import DaemonSet  # noqa: F401, E402
