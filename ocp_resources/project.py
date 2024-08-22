from warnings import warn

from ocp_resources.project_project_openshift_io import Project  # noqa: F401


warn(
    f"The module {__name__} is deprecated and will be removed in version 4.17, "
    "`Project` should be either imported from `ocp_resources.project_project_openshift_io` or "
    "`ocp_resources.project_config_openshift_io` depending on the API group.",
    DeprecationWarning,
    stacklevel=2,
)
