from warnings import warn
from ocp_resources.csi_driver import CSIDriver  # noqa: F401

warn(
    f"The module {__name__} is deprecated and will be removed in version 4.17, `CSIDriver` should be imported from `ocp_resources.csi_driver`",
    DeprecationWarning,
    stacklevel=2,
)
