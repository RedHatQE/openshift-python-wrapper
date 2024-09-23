from warnings import warn
from ocp_resources.config_map import ConfigMap  # noqa: F401

warn(
    f"The module {__name__} is deprecated and will be removed in version 4.17, `ConfigMap` should be "
    "imported from `ocp_resources.config_map`",
    DeprecationWarning,
    stacklevel=2,
)
