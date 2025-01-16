import yaml
from simple_logger.logger import get_logger

LOGGER = get_logger(name=__name__)


def skip_existing_resource_creation_teardown(resource, export_str, user_exported_args, check_exists=True):
    """
    Args:
        resource (Resource): Resource to match against.
        export_str (str): The user export str. (REUSE_IF_RESOURCE_EXISTS or SKIP_RESOURCE_TEARDOWN)
        user_exported_args (str): Value of export_str. (os.environ.get)
        check_exists (bool): Check if resource exists before return. (applied only for REUSE_IF_RESOURCE_EXISTS)

    Returns:
        Resource or None: If resource match.
    """

    def _return_resource(_resource, _check_exists, _msg):
        """
        Return the resource if exists when got _check_exists else return None.
        If _check_exists=False returns the resource.
        """
        if not _check_exists:  # In case of SKIP_RESOURCE_TEARDOWN
            return _resource

        elif _resource.exists:  # In case of REUSE_IF_RESOURCE_EXISTS
            LOGGER.warning(_msg)
            return _resource

    resource.to_dict()
    resource_name = resource.res["metadata"]["name"]
    resource_namespace = resource.res["metadata"].get("namespace")
    skip_create_warn_msg = (
        f"Skip resource {resource.kind} {resource_name} creation, using existing one."
        f" Got {export_str}={user_exported_args}"
    )
    user_args = yaml.safe_load(stream=user_exported_args)
    if resource.kind in user_args:
        _resource_args = user_args[resource.kind]
        if not _resource_args:
            # Match only by kind, user didn't send name and/or namespace.
            return _return_resource(
                _resource=resource,
                _check_exists=check_exists,
                _msg=skip_create_warn_msg,
            )

        for _name, _namespace in _resource_args.items():
            if resource_name == _name and (resource_namespace == _namespace or not (resource_namespace and _namespace)):
                return _return_resource(
                    _resource=resource,
                    _check_exists=check_exists,
                    _msg=skip_create_warn_msg,
                )
