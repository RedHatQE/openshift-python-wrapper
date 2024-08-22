from warnings import warn

from ocp_resources.dns_config_openshift_io import DNS  # noqa: F401

warn(
    f"The module {__name__} is deprecated and will be removed in version 4.17, "
    "`DNS` should be either imported from `ocp_resources.dns_config_openshift_io` "
    "or `ocp_resources.dns_operator_openshift_io`, depending on the API group.",
    DeprecationWarning,
    stacklevel=2,
)
