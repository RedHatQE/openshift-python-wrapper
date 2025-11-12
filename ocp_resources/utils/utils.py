import re

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


def convert_camel_case_to_snake_case(name: str) -> str:
    """
    Converts a camel case string to snake case.

    Args:
        name (str): The camel case string to convert.

    Returns:
        str: The snake case representation of the input string.

    Examples:
        >>> convert_camel_case_to_snake_case(string_="allocateLoadBalancerNodePorts")
        'allocate_load_balancer_node_ports'
        >>> convert_camel_case_to_snake_case(string_="clusterIPs")
        'cluster_ips'
        >>> convert_camel_case_to_snake_case(string_="additionalCORSAllowedOS")
        'additional_cors_allowed_os'

    Notes:
        - This function assumes that the input string adheres to camel case conventions.
        - If the input string contains acronyms (e.g., "XMLHttpRequest"), they will be treated as separate words
          (e.g., "xml_http_request").
        - The function handles both single-word camel case strings (e.g., "Service") and multi-word camel case strings
          (e.g., "myCamelCaseString").
    """
    do_not_process_list = ["oauth", "kubevirt"]

    # If the input string is in the do_not_proccess_list, return it as it is.
    if name.lower() in do_not_process_list:
        return name.lower()

    formatted_str: str = ""

    if name.islower():
        return name

    # For single words, e.g "Service" or "SERVICE"
    if name.istitle() or name.isupper():
        return name.lower()

    # To decide if underscore is needed before a char, keep the last char format.
    # If previous char is uppercase, underscode should not be added. Also applied for the first char in the string.
    last_capital_char: bool | None = None

    # To decide if there are additional words ahead; if found, there is at least one more word ahead, else this is the
    # last word. Underscore should be added before it and all chars from here should be lowercase.
    following_capital_chars: re.Match | None = None

    str_len_for_idx_check = len(name) - 1

    for idx, char in enumerate(name):
        # If lower case, append to formatted string
        if char.islower():
            formatted_str += char
            last_capital_char = False

        # If first char is uppercase
        elif idx == 0:
            formatted_str += char.lower()
            last_capital_char = True

        else:
            if idx < str_len_for_idx_check:
                following_capital_chars = re.search(r"[A-Z]", "".join(name[idx + 1 :]))
            if last_capital_char:
                if idx < str_len_for_idx_check and name[idx + 1].islower():
                    if following_capital_chars:
                        formatted_str += f"_{char.lower()}"
                        last_capital_char = True
                        continue

                    remaining_str = "".join(name[idx:])
                    # The 2 letters in the string; uppercase char followed by lowercase char.
                    # Example: `clusterIPs`, handle `Ps` at this point
                    if idx + 1 == str_len_for_idx_check:
                        formatted_str += remaining_str.lower()
                        break

                    # The last word in the string; uppercase followed by multiple lowercase chars
                    # Example: `dataVolumeTTLSeconds`, handle `Seconds` at this point
                    elif remaining_str.istitle():
                        formatted_str += f"_{remaining_str.lower()}"
                        break

                    else:
                        formatted_str += char.lower()
                        last_capital_char = True

                else:
                    formatted_str += char.lower()
                    last_capital_char = True

            else:
                formatted_str += f"_{char.lower()}"
                last_capital_char = True

    return formatted_str
