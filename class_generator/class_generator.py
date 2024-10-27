from __future__ import annotations

import filecmp
import json
import shlex
import os
import sys
import requests
from pathlib import Path
from packaging.version import Version
import shutil
from tempfile import gettempdir

import textwrap
from typing import Any, Dict, List, Tuple
import click
import re
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
import cloup
from cloup.constraints import If, IsSet, accept_none, require_one
from pyhelper_utils.shell import run_command
import pytest
from rich.console import Console
from rich.syntax import Syntax

from ocp_resources.resource import Resource

from jinja2 import DebugUndefined, Environment, FileSystemLoader, meta
from simple_logger.logger import get_logger


SPEC_STR: str = "SPEC"
FIELDS_STR: str = "FIELDS"
LOGGER = get_logger(name="class_generator")
TESTS_MANIFESTS_DIR: str = "class_generator/tests/manifests"
SCHEMA_DIR: str = "class_generator/schema"
RESOURCES_MAPPING_FILE: str = os.path.join(SCHEMA_DIR, "__resources-mappings.json")
MISSING_DESCRIPTION_STR: str = "No field description from API; please add description"


def _is_kind_and_namespaced(
    client: str, _key: str, _data: Dict[str, Any], kind: str, group: str, version: str
) -> Dict[str, Any]:
    _group_and_version = f"{group}/{version}" if group else version
    not_resource_dict = {"is_kind": False, "kind": _key}

    # if explain command failed, this is not a resource
    if not run_command(command=shlex.split(f"{client} explain {kind}"), check=False, log_errors=False)[0]:
        return not_resource_dict

    api_resources_base_cmd = f"bash -c '{client} api-resources"

    # check if this as a valid version for the resource.
    if run_command(
        command=shlex.split(f"{api_resources_base_cmd} | grep -w {kind} | grep {_group_and_version}'"),
        check=False,
        log_errors=False,
    )[0]:
        # Check if the resource if namespaced.
        _data["namespaced"] = (
            run_command(
                command=shlex.split(
                    f"{api_resources_base_cmd} --namespaced | grep -w {kind} | grep {_group_and_version} | wc -l'"
                ),
                check=False,
                log_errors=False,
            )[1].strip()
            == "1"
        )
        return {"is_kind": True, "kind": _key, "data": _data}

    return not_resource_dict


def map_kind_to_namespaced(client: str, newer_cluster_version: bool, schema_definition_file: Path) -> None:
    not_kind_file: str = os.path.join(SCHEMA_DIR, "__not-kind.txt")

    resources_mapping = read_resources_mapping_file()

    if os.path.isfile(not_kind_file):
        with open(not_kind_file) as fd:
            not_kind_list = fd.read().split("\n")
    else:
        not_kind_list = []

    with open(schema_definition_file) as fd:
        _definitions_json_data = json.load(fd)

    _kind_data_futures: List[Future] = []
    with ThreadPoolExecutor() as executor:
        for _key, _data in _definitions_json_data["definitions"].items():
            if not _data.get("x-kubernetes-group-version-kind"):
                continue

            if _key in not_kind_list:
                continue

            x_kubernetes_group_version_kind = extract_group_kind_version(_kind_schema=_data)
            _kind = x_kubernetes_group_version_kind["kind"]
            _group = x_kubernetes_group_version_kind.get("group", "")
            _version = x_kubernetes_group_version_kind.get("version", "")

            # Do not add the resource if it is already in the mapping and the cluster version is not newer than the last
            if resources_mapping.get(_kind.lower()) and not newer_cluster_version:
                continue

            _kind_data_futures.append(
                executor.submit(
                    _is_kind_and_namespaced,
                    client=client,
                    _key=_key,
                    _data=_data,
                    kind=_kind,
                    group=_group,
                    version=_version,
                )
            )

    _temp_resources_mappings: Dict[Any, Any] = {}
    for res in as_completed(_kind_data_futures):
        _res = res.result()
        # _res["kind"] is group.version.kind, set only kind as key in the final dict
        kind_key = _res["kind"].rsplit(".", 1)[-1].lower()

        if _res["is_kind"]:
            _temp_resources_mappings.setdefault(kind_key, []).append(_res["data"])
        else:
            not_kind_list.append(_res["kind"])

    # Update the resources mapping dict with the one that we filled to avoid duplication in the lists
    resources_mapping.update(_temp_resources_mappings)

    with open(RESOURCES_MAPPING_FILE, "w") as fd:
        json.dump(resources_mapping, fd, indent=4)

    with open(not_kind_file, "w") as fd:
        fd.writelines("\n".join(not_kind_list))


def read_resources_mapping_file() -> Dict[Any, Any]:
    try:
        with open(RESOURCES_MAPPING_FILE) as fd:
            return json.load(fd)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def get_server_version(client: str):
    rc, out, _ = run_command(command=shlex.split(f"{client} version -o json"), check=False)
    if not rc:
        LOGGER.error("Failed to get server version")
        sys.exit(1)

    json_out = json.loads(out)
    return json_out["serverVersion"]["gitVersion"]


def get_client_binary() -> str:
    if os.system("which oc") == 0:
        return "oc"

    elif os.system("which kubectl") == 0:
        return "kubectl"
    else:
        LOGGER.error("Failed to find oc or kubectl")
        sys.exit(1)


def update_kind_schema():
    openapi2jsonschema_str: str = "openapi2jsonschema"
    client = get_client_binary()

    if not run_command(command=shlex.split("which openapi2jsonschema"), check=False, log_errors=False)[0]:
        LOGGER.error(
            f"{openapi2jsonschema_str} not found. Install it using `pipx install --python python3.9 openapi2jsonschema`"
        )
        sys.exit(1)

    rc, token, _ = run_command(command=shlex.split(f"{client} whoami -t"), check=False, log_errors=False)
    if not rc:
        LOGGER.error(
            f"Failed to get token.\nMake sure you are logged in to the cluster using user and password using `{client} login`"
        )
        sys.exit(1)

    api_url = run_command(command=shlex.split(f"{client} whoami --show-server"), check=False, log_errors=False)[
        1
    ].strip()
    data = requests.get(f"{api_url}/openapi/v2", headers={"Authorization": f"Bearer {token.strip()}"}, verify=False)

    if not data.ok:
        LOGGER.error("Failed to get openapi schema.")
        sys.exit(1)

    cluster_version_file = Path("class_generator/__cluster_version__.txt")
    try:
        with open(cluster_version_file, "r") as fd:
            last_cluster_version_generated = fd.read().strip()
    except (FileNotFoundError, IOError) as exp:
        LOGGER.error(f"Failed to read cluster version file: {exp}")
        sys.exit(1)

    cluster_version = get_server_version(client=client)
    cluster_version = cluster_version.split("+")[0]
    ocp_openapi_json_file = Path(gettempdir()) / f"__k8s-openapi-{cluster_version}__.json"
    last_cluster_version_generated: str = ""

    newer_version: bool = Version(cluster_version) > Version(last_cluster_version_generated)

    if newer_version:
        with open(cluster_version_file, "w") as fd:
            fd.write(cluster_version)

    with open(ocp_openapi_json_file, "w") as fd:
        fd.write(data.text)

    tmp_schema_dir = Path(gettempdir()) / f"{SCHEMA_DIR}-{cluster_version}"

    if not run_command(command=shlex.split(f"{openapi2jsonschema_str} {ocp_openapi_json_file} -o {tmp_schema_dir}"))[0]:
        LOGGER.error("Failed to generate schema.")
        sys.exit(1)

    if newer_version:
        # copy all files from tmp_schema_dir to schema dir
        shutil.copytree(src=tmp_schema_dir, dst=SCHEMA_DIR, dirs_exist_ok=True)

    else:
        # Copy only new files from tmp_schema_dir to schema dir
        for root, _, files in os.walk(tmp_schema_dir):
            for file_ in files:
                dst_file = Path(SCHEMA_DIR) / file_
                try:
                    if not os.path.isfile(dst_file):
                        shutil.copy(src=Path(root) / file_, dst=dst_file)
                except (OSError, IOError) as exp:
                    LOGGER.error(f"Failed to copy file {file_}: {exp}")
                    sys.exit(1)

    map_kind_to_namespaced(
        client=client, newer_cluster_version=newer_version, schema_definition_file=ocp_openapi_json_file
    )


def convert_camel_case_to_snake_case(string_: str) -> str:
    """
    Converts a camel case string to snake case.

    Args:
        string_ (str): The camel case string to convert.

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
    do_not_proccess_list = ["OAuth", "KubeVirt"]
    # If the input string is in the do_not_proccess_list, return it as it is.
    if string_.lower() in [_str.lower() for _str in do_not_proccess_list]:
        return string_.lower()

    formatted_str: str = ""

    if string_.islower():
        return string_

    # For single words, e.g "Service" or "SERVICE"
    if string_.istitle() or string_.isupper():
        return string_.lower()

    # To decide if underscore is needed before a char, keep the last char format.
    # If previous char is uppercase, underscode should not be added. Also applied for the first char in the string.
    last_capital_char: bool | None = None

    # To decide if there are additional words ahead; if found, there is at least one more word ahead, else this is the
    # last word. Underscore should be added before it and all chars from here should be lowercase.
    following_capital_chars: re.Match | None = None

    str_len_for_idx_check = len(string_) - 1

    for idx, char in enumerate(string_):
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
                following_capital_chars = re.search(r"[A-Z]", "".join(string_[idx + 1 :]))
            if last_capital_char:
                if idx < str_len_for_idx_check and string_[idx + 1].islower():
                    if following_capital_chars:
                        formatted_str += f"_{char.lower()}"
                        last_capital_char = True
                        continue

                    remaining_str = "".join(string_[idx:])
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


def render_jinja_template(template_dict: Dict[Any, Any], template_dir: str, template_name: str) -> str:
    env = Environment(
        loader=FileSystemLoader(template_dir),
        trim_blocks=True,
        lstrip_blocks=True,
        undefined=DebugUndefined,
    )

    template = env.get_template(name=template_name)
    rendered = template.render(template_dict)
    undefined_variables = meta.find_undeclared_variables(env.parse(rendered))

    if undefined_variables:
        LOGGER.error(f"The following variables are undefined: {undefined_variables}")
        sys.exit(1)

    return rendered


def parse_user_code_from_file(file_path: str) -> str:
    with open(file_path) as fd:
        data = fd.read()

    line = "    # End of generated code"
    if line in data:
        _end_of_generated_code_index = data.index(line)
        _user_code = data[_end_of_generated_code_index + len(line) :]
        return _user_code

    return ""


def generate_resource_file_from_dict(
    resource_dict: Dict[str, Any],
    overwrite: bool = False,
    dry_run: bool = False,
    output_file: str = "",
    add_tests: bool = False,
    output_file_suffix: str = "",
    output_dir: str = "",
) -> Tuple[str, str]:
    base_dir = output_dir or "ocp_resources"
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    rendered = render_jinja_template(
        template_dict=resource_dict,
        template_dir="class_generator/manifests",
        template_name="class_generator_template.j2",
    )

    formatted_kind_str = convert_camel_case_to_snake_case(string_=resource_dict["kind"])
    _file_suffix: str = f"{'_' + output_file_suffix if output_file_suffix else ''}"

    if add_tests:
        overwrite = True
        tests_path = os.path.join(TESTS_MANIFESTS_DIR, resource_dict["kind"])
        if not os.path.exists(tests_path):
            os.makedirs(tests_path)

        _output_file = os.path.join(tests_path, f"{formatted_kind_str}{_file_suffix}.py")

    elif output_file:
        _output_file = output_file

    else:
        _output_file = os.path.join(base_dir, f"{formatted_kind_str}{_file_suffix}.py")

    _output_file_exists: bool = os.path.exists(_output_file)
    _user_code: str = ""

    if _output_file_exists:
        _user_code = parse_user_code_from_file(file_path=_output_file)

    orig_filename = _output_file
    if _output_file_exists:
        if overwrite:
            LOGGER.warning(f"Overwriting {_output_file}")

        else:
            temp_output_file = _output_file.replace(".py", "_TEMP.py")
            LOGGER.warning(f"{_output_file} already exists, using {temp_output_file}")
            _output_file = temp_output_file

    if dry_run:
        if _user_code:
            rendered += _user_code
        _code = Syntax(code=rendered, lexer="python", line_numbers=True)
        Console().print(_code)

    else:
        write_and_format_rendered(filepath=_output_file, data=rendered, user_code=_user_code)

    return orig_filename, _output_file


def types_generator(key_dict: Dict[str, Any]) -> Dict[str, str]:
    type_for_docstring: str = "Any"
    type_from_dict_for_init: str = ""
    # A resource field may be defined with `x-kubernetes-preserve-unknown-fields`. In this case, `type` is not provided.
    resource_type = key_dict.get("type")

    # All fields must be set with Optional since resource can have yaml_file to cover all args.
    if resource_type == "array":
        type_for_docstring = "List[Any]"

    elif resource_type == "string":
        type_for_docstring = "str"
        type_from_dict_for_init = f'Optional[{type_for_docstring}] = ""'

    elif resource_type == "boolean":
        type_for_docstring = "bool"

    elif resource_type == "integer":
        type_for_docstring = "int"

    elif resource_type == "object":
        type_for_docstring = "Dict[str, Any]"

    if not type_from_dict_for_init:
        type_from_dict_for_init = f"Optional[{type_for_docstring}] = None"

    return {"type-for-init": type_from_dict_for_init, "type-for-doc": type_for_docstring}


def get_property_schema(property_: Dict[str, Any]) -> Dict[str, Any]:
    if _ref := property_.get("$ref"):
        with open(f"{SCHEMA_DIR}/{_ref.rsplit('.')[-1].lower()}.json") as fd:
            return json.load(fd)
    return property_


def format_description(description: str) -> str:
    _res = ""
    _text = textwrap.wrap(text=description, subsequent_indent="    ")
    for _txt in _text:
        _res += f"{_txt}\n"

    return _res


def prepare_property_dict(
    schema: Dict[str, Any],
    required: List[str],
    resource_dict: Dict[str, Any],
    dict_key: str,
) -> Dict[str, Any]:
    keys_to_ignore: List[str] = ["kind", "apiVersion", "status", SPEC_STR.lower()]
    keys_to_rename: set[str] = {"annotations", "labels"}
    if dict_key != SPEC_STR.lower():
        keys_to_ignore.append("metadata")

    for key, val in schema.items():
        if key in keys_to_ignore:
            continue

        val_schema = get_property_schema(property_=val)
        type_dict = types_generator(key_dict=val_schema)
        python_name = convert_camel_case_to_snake_case(string_=f"{dict_key}_{key}" if key in keys_to_rename else key)
        resource_dict[dict_key].append({
            "name-for-class-arg": python_name,
            "property-name": key,
            "required": key in required,
            "description": format_description(description=val_schema.get("description", MISSING_DESCRIPTION_STR)),
            "type-for-docstring": type_dict["type-for-doc"],
            "type-for-class-arg": f"{python_name}: {type_dict['type-for-init']}",
        })

    return resource_dict


def parse_explain(
    kind: str,
) -> List[Dict[str, Any]]:
    _schema_definition = read_resources_mapping_file()
    _resources: List[Dict[str, Any]] = []

    _kinds_schema = _schema_definition[kind.lower()]
    for _kind_schema in _kinds_schema:
        namespaced = _kind_schema["namespaced"]
        resource_dict: Dict[str, Any] = {
            "base_class": "NamespacedResource" if namespaced else "Resource",
            "description": _kind_schema.get("description", MISSING_DESCRIPTION_STR),
            "fields": [],
            "spec": [],
        }

        schema_properties: Dict[str, Any] = _kind_schema.get("properties", {})
        fields_required = _kind_schema.get("required", [])

        resource_dict.update(extract_group_kind_version(_kind_schema=_kind_schema))

        if spec_schema := schema_properties.get("spec", {}):
            spec_schema = get_property_schema(property_=spec_schema)
            spec_required = spec_schema.get("required", [])
            resource_dict = prepare_property_dict(
                schema=spec_schema.get("properties", {}),
                required=spec_required,
                resource_dict=resource_dict,
                dict_key="spec",
            )

        resource_dict = prepare_property_dict(
            schema=schema_properties,
            required=fields_required,
            resource_dict=resource_dict,
            dict_key="fields",
        )

        api_group_real_name = resource_dict.get("group")
        # If API Group is not present in resource, try to get it from VERSION
        if not api_group_real_name:
            version_splited = resource_dict["version"].split("/")
            if len(version_splited) == 2:
                api_group_real_name = version_splited[0]

        if api_group_real_name:
            api_group_for_resource_api_group = api_group_real_name.upper().replace(".", "_").replace("-", "_")
            resource_dict["group"] = api_group_for_resource_api_group
            missing_api_group_in_resource: bool = not hasattr(Resource.ApiGroup, api_group_for_resource_api_group)

            if missing_api_group_in_resource:
                LOGGER.warning(
                    f"Missing API Group in Resource\n"
                    f"Please add `Resource.ApiGroup.{api_group_for_resource_api_group} = {api_group_real_name}` "
                    "manually into ocp_resources/resource.py under Resource class > ApiGroup class."
                )

        else:
            api_version_for_resource_api_version = resource_dict["version"].upper()
            missing_api_version_in_resource: bool = not hasattr(
                Resource.ApiVersion, api_version_for_resource_api_version
            )

            if missing_api_version_in_resource:
                LOGGER.warning(
                    f"Missing API Version in Resource\n"
                    f"Please add `Resource.ApiVersion.{api_version_for_resource_api_version} = {resource_dict['version']}` "
                    "manually into ocp_resources/resource.py under Resource class > ApiGroup class."
                )

        _resources.append(resource_dict)

    return _resources


def extract_group_kind_version(_kind_schema: Dict[str, Any]) -> Dict[str, str]:
    group_kind_versions: List[Dict[str, str]] = _kind_schema["x-kubernetes-group-version-kind"]
    group_kind_version = group_kind_versions[0]

    for group_kind_version in group_kind_versions:
        if group_kind_version.get("group"):
            break

    return group_kind_version


def class_generator(
    kind: str,
    overwrite: bool = False,
    dry_run: bool = False,
    output_file: str = "",
    output_dir: str = "",
    add_tests: bool = False,
    called_from_cli: bool = True,
) -> List[str]:
    """
    Generates a class for a given Kind.
    """
    LOGGER.info(f"Generating class for {kind}")
    kind = kind.lower()
    kind_and_namespaced_mappings = read_resources_mapping_file().get(kind)

    if not kind_and_namespaced_mappings:
        LOGGER.error(f"{kind} not found in {RESOURCES_MAPPING_FILE}, Please run with --update-schema")
        if called_from_cli:
            sys.exit(1)
        else:
            return []

    resources = parse_explain(kind=kind)

    use_output_file_suffix: bool = len(resources) > 1
    generated_files: List[str] = []
    for resource_dict in resources:
        output_file_suffix = resource_dict["group"].lower() if use_output_file_suffix else ""

        orig_filename, generated_py_file = generate_resource_file_from_dict(
            resource_dict=resource_dict,
            overwrite=overwrite,
            dry_run=dry_run,
            output_file=output_file,
            add_tests=add_tests,
            output_file_suffix=output_file_suffix,
            output_dir=output_dir,
        )

        if not dry_run:
            run_command(
                command=shlex.split(f"uvx pre-commit run --files {generated_py_file}"),
                verify_stderr=False,
                check=False,
            )

            if orig_filename != generated_py_file and filecmp.cmp(orig_filename, generated_py_file):
                LOGGER.warning(f"File {orig_filename} was not updated, deleting {generated_py_file}")
                Path.unlink(Path(generated_py_file))

        generated_files.append(generated_py_file)

    return generated_files


def write_and_format_rendered(filepath: str, data: str, user_code: str = "") -> None:
    with open(filepath, "w") as fd:
        fd.write(data)

        if user_code:
            fd.write(user_code)

    for op in ("format", "check"):
        run_command(
            command=shlex.split(f"uvx ruff {op} {filepath}"),
            verify_stderr=False,
            check=False,
        )


def generate_class_generator_tests() -> None:
    tests_info: Dict[str, List[Dict[str, str]]] = {"template": []}
    dirs_to_ignore: List[str] = ["__pycache__"]

    for _dir in os.listdir(TESTS_MANIFESTS_DIR):
        if _dir in dirs_to_ignore:
            continue

        dir_path = os.path.join(TESTS_MANIFESTS_DIR, _dir)
        if os.path.isdir(dir_path):
            test_data = {"kind": _dir}

            for _file in os.listdir(dir_path):
                if _file.endswith("_res.py"):
                    test_data["res_file"] = _file

            tests_info["template"].append(test_data)

    rendered = render_jinja_template(
        template_dict=tests_info,
        template_dir=TESTS_MANIFESTS_DIR,
        template_name="test_parse_explain.j2",
    )

    write_and_format_rendered(
        filepath=os.path.join(Path(TESTS_MANIFESTS_DIR).parent, "test_class_generator.py"),
        data=rendered,
    )


@cloup.command("Resource class generator", show_constraints=True)
@cloup.option(
    "-k",
    "--kind",
    type=click.STRING,
    help="""
    \b
    The Kind to generate the class for, Needs working cluster with admin privileges.
    multiple kinds can be sent separated by comma (without psaces)
    Example: -k Deployment,Pod,ConfigMap
""",
)
@cloup.option(
    "-o",
    "--output-file",
    help="The full filename path to generate a python resource file. If not sent, resource kind will be used",
    type=click.Path(),
)
@cloup.option(
    "--overwrite",
    is_flag=True,
    help="Output file overwrite existing file if passed",
)
@cloup.option("--dry-run", is_flag=True, help="Run the script without writing to file")
@cloup.option(
    "--add-tests",
    help=f"Add a test to `test_class_generator.py` and test files to `{TESTS_MANIFESTS_DIR}` dir",
    is_flag=True,
    show_default=True,
)
@cloup.option(
    "--update-schema",
    help="Update kind schema files",
    is_flag=True,
    show_default=True,
)
@cloup.constraint(
    If("update_schema", then=accept_none),
    ["add_tests", "dry_run", "kind", "output_file", "overwrite"],
)
@cloup.constraint(
    If(
        IsSet("add_tests"),
        then=accept_none,
    ),
    ["output_file", "dry_run", "update_schema", "overwrite"],
)
@cloup.constraint(require_one, ["kind", "update_schema"])
def main(
    kind: str,
    overwrite: bool,
    dry_run: bool,
    output_file: str,
    add_tests: bool,
    update_schema: bool,
) -> None:
    if update_schema:
        return update_kind_schema()

    _kwargs: Dict[str, Any] = {
        "overwrite": overwrite,
        "dry_run": dry_run,
        "output_file": output_file,
        "add_tests": add_tests,
    }

    kinds: List[str] = kind.split(",")
    futures: List[Future] = []

    with ThreadPoolExecutor() as executor:
        for _kind in kinds:
            _kwargs["kind"] = _kind

            if len(kinds) == 1:
                class_generator(**_kwargs)

            else:
                executor.submit(
                    class_generator,
                    **_kwargs,
                )

        for _ in as_completed(futures):
            # wait for all tasks to complete
            pass

    if add_tests:
        generate_class_generator_tests()
        pytest.main(["-k", "test_class_generator"])


if __name__ == "__main__":
    main()
