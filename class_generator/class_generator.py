from __future__ import annotations

import ast
import filecmp
import json
import shlex
import os
import sys
from pathlib import Path

import textwrap
from typing import Any, Dict, List, Optional, Set, Tuple
import click
import re
import requests
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
import cloup
from cloup.constraints import If, IsSet, accept_none, require_one
from pyhelper_utils.shell import run_command
import pytest
from rich.console import Console
from rich.syntax import Syntax
import astor

from ocp_resources.resource import Resource

from jinja2 import DebugUndefined, Environment, FileSystemLoader, meta
from simple_logger.logger import get_logger


SPEC_STR: str = "SPEC"
FIELDS_STR: str = "FIELDS"
LOGGER = get_logger(name="class_generator")
TESTS_MANIFESTS_DIR: str = "class_generator/tests/manifests"
SCHEMA_DIR: str = "class_generator/schema"
RESOURCES_MAPPING_FILE: str = os.path.join(SCHEMA_DIR, "__resources-mappings.json")


def _is_kind_is_namespaced(_kind: str) -> Tuple[bool, str]:
    return (
        run_command(
            command=shlex.split(f"bash -c 'oc api-resources --namespaced | grep -w {_kind} | wc -l'"),
            check=False,
        )[1].strip()
        == "1"
    ), _kind


def _is_resource(_kind: str) -> Tuple[bool, str]:
    return (
        run_command(command=shlex.split(f"oc explain {_kind}"), check=False, log_errors=False)[0],
        _kind,
    )


def map_kind_to_namespaced():
    not_kind_file: str = os.path.join(SCHEMA_DIR, "__not-kind.txt")

    not_kind_list: List[str] = []
    if os.path.isfile(not_kind_file):
        with open(not_kind_file) as fd:
            not_kind_list = fd.read().split("\n")

    with open(os.path.join(f"{SCHEMA_DIR}/all.json")) as fd:
        all_json_data = json.load(fd)

    resources_mapping: Dict[str, Dict[str, bool]] = {}
    if os.path.isfile(RESOURCES_MAPPING_FILE):
        resources_mapping = read_resources_mapping_file()

    # `all.json` list all files that `openapi2jsonschema` generated which include duplication
    kind_set: Set[str] = set()
    for _def in all_json_data["oneOf"]:
        _kind = _def["$ref"].rsplit(".", 1)[-1]
        if _kind in not_kind_list:
            continue

        kind_set.add(_kind)

    kind_list: List[str] = []
    is_kind_futures: List[Future] = []
    with ThreadPoolExecutor() as executor:
        for _kind in kind_set:
            if resources_mapping.get(_kind.lower()):  # resource_mappings store all keys in lowercase
                continue

            # Check if the kind we work on is a real kind
            is_kind_futures.append(executor.submit(_is_resource, _kind=_kind))

    for _res in as_completed(is_kind_futures):
        res = _res.result()

        if res[0]:
            kind_list.append(res[1])
        else:
            not_kind_list.append(res[1])

    mapping_kind_futures: List[Future] = []
    with ThreadPoolExecutor() as executor:
        for _kind in kind_list:
            mapping_kind_futures.append(executor.submit(_is_kind_is_namespaced, _kind=_kind))

    for _res in as_completed(mapping_kind_futures):
        res = _res.result()
        resources_mapping[res[1].lower()] = {"namespaced": res[0]}

    with open(RESOURCES_MAPPING_FILE, "w") as fd:
        json.dump(resources_mapping, fd)

    with open(not_kind_file, "w") as fd:
        fd.writelines("\n".join(not_kind_list))


def read_resources_mapping_file() -> Dict[Any, Any]:
    with open(RESOURCES_MAPPING_FILE) as fd:
        return json.load(fd)


def update_kind_schema():
    openapi2jsonschema_str: str = "openapi2jsonschema"

    if not run_command(command=shlex.split("which openapi2jsonschema"), check=False, log_errors=False)[0]:
        LOGGER.error(
            f"{openapi2jsonschema_str}not found. Install it using `pipx install --python python3.9 openapi2jsonschema`"
        )
        sys.exit(1)

    rc, token, _ = run_command(command=shlex.split("oc whoami -t"), check=False, log_errors=False)
    if not rc:
        LOGGER.error(
            "Failed to get token.\nMake sure you are logged in to the cluster using user and password using `oc login`"
        )
        sys.exit(1)

    api_url = run_command(command=shlex.split("oc whoami --show-server"), check=False, log_errors=False)[1].strip()
    data = requests.get(
        f"{api_url}/openapi/v2",
        headers={"Authorization": f"Bearer {token.strip()}"},
        verify=False,
    )

    if not data.ok:
        LOGGER.error("Failed to get openapi schema.")
        sys.exit(1)

    ocp_openapi_json_file = "class_generator/__ocp-openapi.json"
    with open(ocp_openapi_json_file, "w") as fd:
        fd.write(data.text)

    if not run_command(command=shlex.split(f"{openapi2jsonschema_str} {ocp_openapi_json_file} -o {SCHEMA_DIR}"))[0]:
        LOGGER.error("Failed to generate schema.")
        sys.exit(1)

    map_kind_to_namespaced()


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


def generate_resource_file_from_dict(
    resource_dict: Dict[str, Any],
    overwrite: bool = False,
    dry_run: bool = False,
    output_file: str = "",
    add_tests: bool = False,
) -> Tuple[str, str]:
    rendered = render_jinja_template(
        template_dict=resource_dict,
        template_dir="class_generator/manifests",
        template_name="class_generator_template.j2",
    )

    formatted_kind_str = convert_camel_case_to_snake_case(string_=resource_dict["kind"])
    if add_tests:
        overwrite = True
        _output_file = os.path.join(TESTS_MANIFESTS_DIR, resource_dict["kind"], f"{formatted_kind_str}_res.py")

    elif output_file:
        _output_file = output_file

    else:
        _output_file = os.path.join("ocp_resources", f"{formatted_kind_str}.py")

    orig_filename = _output_file
    if os.path.exists(_output_file):
        if overwrite:
            LOGGER.warning(f"Overwriting {_output_file}")

        else:
            temp_output_file = _output_file.replace(".py", "_TEMP.py")
            LOGGER.warning(f"{_output_file} already exists, using {temp_output_file}")
            _output_file = temp_output_file

    if dry_run:
        _code = Syntax(code=rendered, lexer="python", line_numbers=True)
        Console().print(_code)

    else:
        write_and_format_rendered(filepath=_output_file, data=rendered)

    return orig_filename, _output_file


def types_generator(key_dict: Dict[str, Any]) -> Dict[str, str]:
    type_for_docstring: str = "Dict[str, Any]"
    type_from_dict_for_init: str = ""

    # All fields must be set with Optional since resource can have yaml_file to cover all args.
    if key_dict["type"] == "array":
        type_for_docstring = "List[Any]"

    elif key_dict == "string":
        type_for_docstring = "str"
        type_from_dict_for_init = f'Optional[{type_for_docstring}] = ""'

    elif key_dict == "boolean":
        type_for_docstring = "bool"

    elif key_dict == "integer":
        type_for_docstring = "int"

    if not type_from_dict_for_init:
        type_from_dict_for_init = f"Optional[{type_for_docstring}] = None"

    return {
        "type-for-init": type_from_dict_for_init,
        "type-for-doc": type_for_docstring,
    }


def get_property_schema(property: Dict[str, Any]) -> Dict[str, Any]:
    if _ref := property.get("$ref"):
        with open(f"{SCHEMA_DIR}/{_ref.rsplit('.')[-1].lower()}.json") as fd:
            return json.load(fd)
    return property


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
    for key, val in schema.items():
        if key in {"metadata", "kind", "apiVersion", "status", SPEC_STR.lower()}:
            continue

        val_schema = get_property_schema(property=val)
        type_dict = types_generator(key_dict=val_schema)
        python_name = convert_camel_case_to_snake_case(string_=key)
        resource_dict[dict_key].append({
            "name-for-class-arg": python_name,
            "property-name": key,
            "required": key in required,
            "description": format_description(description=val_schema["description"]),
            "type-for-docstring": type_dict["type-for-doc"],
            "type-for-class-arg": f"{python_name}: {type_dict['type-for-init']}",
        })

    return resource_dict


def parse_explain(
    kind_schema_file: str,
    namespaced: Optional[bool] = None,
) -> Dict[str, Any]:
    with open(kind_schema_file) as fd:
        kind_schema = json.load(fd)

    resource_dict: Dict[str, Any] = {
        "base_class": "NamespacedResource" if namespaced else "Resource",
        "description": kind_schema["description"],
        "fields": [],
        "spec": [],
    }

    schema_properties: Dict[str, Any] = kind_schema["properties"]
    fields_requeired = kind_schema.get("required", [])
    resource_dict.update(kind_schema["x-kubernetes-group-version-kind"][0])

    if spec_schema := schema_properties.get("spec", {}):
        spec_schema = get_property_schema(property=spec_schema)
        spec_requeired = spec_schema.get("required", [])
        resource_dict = prepare_property_dict(
            schema=spec_schema.get("properties", {}),
            required=spec_requeired,
            resource_dict=resource_dict,
            dict_key="spec",
        )

    resource_dict = prepare_property_dict(
        schema=schema_properties,
        required=fields_requeired,
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
        api_group_for_resource_api_group = api_group_real_name.upper().replace(".", "_")
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
        missing_api_version_in_resource: bool = not hasattr(Resource.ApiVersion, api_version_for_resource_api_version)

        if missing_api_version_in_resource:
            LOGGER.warning(
                f"Missing API Version in Resource\n"
                f"Please add `Resource.ApiVersion.{api_version_for_resource_api_version} = {resource_dict['version']}` "
                "manually into ocp_resources/resource.py under Resource class > ApiGroup class."
            )

    return resource_dict


def get_kind_schema_file(kind: str) -> str:
    kind_file = os.path.join(SCHEMA_DIR, f"{kind.lower()}.json")
    if os.path.isfile(kind_file):
        return kind_file

    LOGGER.error(f"{kind} schema not found, please run with `--update-schema`")
    sys.exit(1)


def class_generator(
    kind: str,
    overwrite: bool = False,
    dry_run: bool = False,
    output_file: str = "",
    add_tests: bool = False,
) -> str:
    """
    Generates a class for a given Kind.
    """
    kind = kind.lower()
    kind_and_namespaced_mappings = read_resources_mapping_file().get(kind)

    if not kind_and_namespaced_mappings:
        LOGGER.error(f"{kind} not found in {RESOURCES_MAPPING_FILE}, Please run with --update-schema")
        sys.exit(1)

    resource_dict = parse_explain(
        kind_schema_file=get_kind_schema_file(kind=kind),
        namespaced=kind_and_namespaced_mappings["namespaced"],
    )
    if not resource_dict:
        return ""

    orig_filename, generated_py_file = generate_resource_file_from_dict(
        resource_dict=resource_dict,
        overwrite=overwrite,
        dry_run=dry_run,
        output_file=output_file,
        add_tests=add_tests,
    )

    if not dry_run:
        run_command(
            command=shlex.split(f"pre-commit run --files {generated_py_file}"),
            verify_stderr=False,
            check=False,
        )

        if orig_filename != generated_py_file:
            if filecmp.cmp(orig_filename, generated_py_file):
                LOGGER.warning(f"File {orig_filename} was not updated, deleting {generated_py_file}")
                Path.unlink(Path(generated_py_file))
            else:
                combine_python_files(original_file=orig_filename, generated_file=generated_py_file)

    return generated_py_file


def combine_python_files(original_file: str, generated_file: str) -> None:
    with open(original_file) as file:
        original_tree: ast.Module = ast.parse(file.read())

    with open(generated_file) as file:
        generated_tree: ast.Module = ast.parse(file.read())

    original_nodes: List[Any] = [
        node for node in original_tree.body if not isinstance(node, (ast.Import, ast.ImportFrom))
    ]
    generated_nodes: List[Any] = [
        node for node in generated_tree.body if not isinstance(node, (ast.Import, ast.ImportFrom))
    ]

    combined_imported_comments: List[Any] = _get_combined_imports_comments(
        generated_tree=generated_tree, original_tree=original_tree
    )

    for node in original_nodes:
        # If the node is the resource class, we need to reconstruct it
        if isinstance(node, ast.ClassDef) and node.bases[0].id in (  # type: ignore[attr-defined]
            "Resource",
            "NamespacedResource",
        ):
            for index, sub_node in enumerate(node.body):
                for generated_node in generated_nodes:
                    if isinstance(generated_node, ast.ClassDef) and generated_node.bases[0].id in (  # type: ignore[attr-defined]
                        "Resource",
                        "NamespacedResource",
                    ):
                        for _sub_node in generated_node.body:
                            if isinstance(_sub_node, type(sub_node)):
                                if isinstance(_sub_node, ast.AnnAssign):
                                    node.body[index] = _sub_node
                                    break

                                elif isinstance(_sub_node, ast.Expr):
                                    node.body[index] = _sub_node
                                    break

                                elif isinstance(_sub_node, ast.Attribute):
                                    node.body[index] = _sub_node
                                    break

                                elif isinstance(_sub_node, ast.FunctionDef) and _sub_node.name == sub_node.name:  # type: ignore[attr-defined]
                                    node.body[index] = _sub_node
                                    break

    new_tree = ast.Module(body=combined_imported_comments + original_nodes, type_ignores=[])

    new_code = astor.to_source(new_tree)

    with open(generated_file, "w") as file:
        file.write(new_code)

    run_command(
        command=shlex.split(f"poetry run ruff format {generated_file}"),
        verify_stderr=False,
        check=False,
    )


def _get_combined_imports_comments(
    generated_tree: ast.Module, original_tree: ast.Module
) -> List[ast.Import | ast.ImportFrom]:
    imports = [node for node in generated_tree.body if isinstance(node, (ast.Import, ast.ImportFrom))]

    imports.extend([node for node in original_tree.body if isinstance(node, (ast.Import, ast.ImportFrom))])

    return imports


def write_and_format_rendered(filepath: str, data: str) -> None:
    with open(filepath, "w") as fd:
        fd.write(data)

    for op in ("format", "check"):
        run_command(
            command=shlex.split(f"poetry run ruff {op} {filepath}"),
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
