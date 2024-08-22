from warnings import warn

from ocp_resources.nm_state import NMState  # noqa: F401

warn(
    f"The module {__name__} is deprecated and will be removed in version 4.17, "
    "`NMState` should be imported from `ocp_resources.nm_state`",
    DeprecationWarning,
    stacklevel=2,
)
