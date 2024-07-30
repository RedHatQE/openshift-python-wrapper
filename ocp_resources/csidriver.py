from warnings import warn
from ocp_resources.csi_driver import CSIDriver  # noqa: F401

warn(
    f"The module {__name__} is deprecated. `CSIDriver` should be imported from `ocp_resources.csi_driver`",
    DeprecationWarning,
    stacklevel=2,
)
