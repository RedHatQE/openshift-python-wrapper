from warnings import warn

from ocp_resources.network_config_openshift_io import Network  # noqa: F401

warn(
    f"The module {__name__} is deprecated and will be removed in version 4.17, "
    "`Network` should be either imported from `ocp_resources.network_config_openshift_io` or "
    "`ocp_resources.network_operator_openshift_io` depending on the API group.",
    DeprecationWarning,
    stacklevel=2,
)
