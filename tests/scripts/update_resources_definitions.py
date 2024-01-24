import shlex
import subprocess
import json
from json import JSONDecodeError


def resources_dict_from_api_resources():
    """
    Build dict with resources and matched values.

    Output example for resource:
    {
        'api_version': 'networking.k8s.io/v1',
        'api_group': {'config.openshift.io': 'false', 'networking.k8s.io': 'true'}
    }
    """
    resources_dict = {}
    api_resources = subprocess.check_output(shlex.split("oc api-resources --no-headers"))
    api_resources = api_resources.decode("utf-8")
    for line in api_resources.splitlines():
        line_list = line.split()
        try:
            _, _, api_version, namespaced, kind = line_list
        except ValueError:
            _, api_version, namespaced, kind = line_list

        split_api_version = api_version.split("/")
        api_group = split_api_version[0] if len(split_api_version) > 1 else None
        resources_dict.setdefault(kind, {}).setdefault("api_group", {})
        resources_dict[kind]["api_group"].update({api_group: {}})
        resources_dict[kind]["api_group"][api_group]["namespaced"] = namespaced
        resources_dict[kind]["api_group"][api_group]["api_version"] = split_api_version[-1]

    return resources_dict


if __name__ == "__main__":
    data_file = "tests/scripts/resources_definitions.json"
    with open(data_file, "r") as fd_read:
        try:
            data = json.loads(fd_read.read())
        except JSONDecodeError:
            data = {}

    new_data = resources_dict_from_api_resources()
    if new_data:
        for key in new_data:
            data[key] = new_data[key]

        with open(data_file, "w") as fd_write:
            fd_write.write(json.dumps(data))
