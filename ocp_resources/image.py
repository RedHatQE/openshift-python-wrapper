from warnings import warn

from ocp_resources.image_image_openshift_io import Image  # noqa: F401

warn(
    f"The module {__name__} is deprecated and will be removed in version 4.17, "
    "`Image` should be either imported from `ocp_resources.image_image_openshift_io` or "
    "`ocp_resources.image_config_openshift_io` depending on the API group.",
    DeprecationWarning,
    stacklevel=2,
)
