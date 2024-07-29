from __future__ import annotations
import json
import shlex
import os
import sys

from typing import Any, Dict, List, Optional, Tuple
import click
import re

from pyhelper_utils.shell import run_command
from rich.console import Console

from rich.prompt import Prompt
from ocp_resources.resource import Resource

from jinja2 import DebugUndefined, Environment, FileSystemLoader, meta
from simple_logger.logger import get_logger

SPEC_STR: str = "SPEC"
FIELDS_STR: str = "FIELDS"

TYPE_MAPPING: Dict[str, str] = {
    "<integer>": "int",
    "<Object>": "Dict[Any, Any]",
    "<[]Object>": "List[Any]",
    "<string>": "str",
    "<map[string]string>": "Dict[Any, Any]",
    "<boolean>": "bool",
}
LOGGER = get_logger(name="class_generator")


def get_oc_or_kubectl() -> str:
    if run_command(command=shlex.split("which oc"), check=False)[0]:
        return "oc"

    elif run_command(command=shlex.split("which kubectl"), check=False)[0]:
        return "kubectl"

    else:
        LOGGER.error("oc or kubectl not available")
        sys.exit(1)


def check_cluster_available() -> bool:
    _exec = get_oc_or_kubectl()
    if not _exec:
        return False

    return run_command(command=shlex.split(f"{_exec} version"), check=False)[0]


def write_to_file(kind: str, data: Dict[str, Any], output_debug_file_path: str) -> None:
    content = {}
    if os.path.isfile(output_debug_file_path):
        with open(output_debug_file_path) as fd:
            content = json.load(fd)

    content.update(data)
    with open(output_debug_file_path, "w") as fd:
        json.dump(content, fd, indent=4)


def get_kind_data(kind: str, debug: bool = False, output_debug_file_path: str = "") -> Dict[str, Any]:
    """
    Get oc/kubectl explain output for given kind and if kind is namespaced
    """
    _, explain_out, _ = run_command(command=shlex.split(f"oc explain {kind} --recursive"))
    if debug:
        write_to_file(
            kind=kind,
            data={"explain": explain_out},
            output_debug_file_path=output_debug_file_path,
        )

    resource_kind = re.search(r".*?KIND:\s+(.*?)\n", explain_out)
    if not resource_kind:
        LOGGER.error(f"Failed to get resource kind from explain for {kind}")
        return {}

    _, namespace_out, _ = run_command(
        command=shlex.split(f"bash -c 'oc api-resources --namespaced | grep -w {resource_kind.group(1)} | wc -l'"),
        check=False,
    )
    if debug:
        write_to_file(
            kind=kind,
            data={"namespace": namespace_out},
            output_debug_file_path=output_debug_file_path,
        )

    if namespace_out.strip() == "1":
        return {"data": explain_out, "namespaced": True}

    return {"data": explain_out, "namespaced": False}


def format_resource_kind(resource_kind: str) -> str:
    """Convert CamelCase to snake_case"""
    return re.sub(r"(?<!^)(?<=[a-z])(?=[A-Z])", "_", resource_kind).lower().strip()


def get_field_description(
    kind: str,
    field_name: str,
    field_under_spec: bool,
    debug: bool,
    output_debug_file_path: str = "",
    debug_content: Optional[Dict[str, str]] = None,
) -> str:
    if debug_content:
        _out = debug_content[f"explain-{field_name}"]

    else:
        _, _out, _ = run_command(
            command=shlex.split(f"oc explain {kind}{'.spec' if field_under_spec else ''}.{field_name}"),
            check=False,
            verify_stderr=False,
        )

    if debug:
        write_to_file(
            kind=kind,
            data={f"explain-{field_name}": _out},
            output_debug_file_path=output_debug_file_path,
        )

    _description = re.search(r"DESCRIPTION:\n\s*(.*)", _out, re.DOTALL)
    if _description:
        description: str = ""
        _fields_found = False
        for line in _description.group(1).strip().splitlines():
            if line.strip():
                if line.startswith("FIELDS:"):
                    _fields_found = True
                    description += f"{' ' * 4}{line}\n"
                else:
                    indent = 4 if _fields_found else 0
                    description += f"{' ' * indent}{line}\n"
            else:
                indent = 8 if _fields_found else 4
                description += f"{' ' * indent}{line}\n"

        return f"{description}\n"

    return "<please add description>"


def get_arg_params(
    field: str,
    kind: str,
    field_under_spec: bool = False,
    debug: bool = False,
    output_debug_file_path: str = "",
    debug_content: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    splited_field = field.split()
    _orig_name, _type = splited_field[0], splited_field[1]

    name = format_resource_kind(resource_kind=_orig_name)
    type_ = _type.strip()
    required: bool = "-required-" in splited_field
    type_from_dict: str = TYPE_MAPPING.get(type_, "Dict[Any, Any]")
    type_from_dict_for_init = type_from_dict

    # All fields must be set with Optional since resource can have yaml_file to cover all args.
    if type_from_dict == "Dict[Any, Any]":
        type_from_dict_for_init = "Optional[Dict[str, Any]] = None"

    if type_from_dict == "List[Any]":
        type_from_dict_for_init = "Optional[List[Any]] = None"

    if type_from_dict == "str":
        type_from_dict_for_init = 'Optional[str] = ""'

    if type_from_dict == "bool":
        type_from_dict_for_init = "Optional[bool] = None"

    if type_from_dict == "int":
        type_from_dict_for_init = "Optional[int] = None"

    _res: Dict[str, Any] = {
        "name-from-explain": _orig_name,
        "name-for-class-arg": name,
        "type-for-class-arg": f"{name}: {type_from_dict_for_init}",
        "required": required,
        "type": type_from_dict,
        "description": get_field_description(
            kind=kind,
            field_name=_orig_name,
            field_under_spec=field_under_spec,
            debug=debug,
            output_debug_file_path=output_debug_file_path,
            debug_content=debug_content,
        ),
    }

    return _res


def generate_resource_file_from_dict(
    resource_dict: Dict[str, Any],
    output_dir="ocp_resources",
    overwrite: bool = False,
    dry_run: bool = False,
) -> str:
    env = Environment(
        loader=FileSystemLoader("scripts/resource/manifests"),
        trim_blocks=True,
        lstrip_blocks=True,
        undefined=DebugUndefined,
        autoescape=True,
    )

    template = env.get_template(name="class_generator_template.j2")
    rendered = template.render(resource_dict)
    undefined_variables = meta.find_undeclared_variables(env.parse(rendered))
    if undefined_variables:
        LOGGER.error(f"The following variables are undefined: {undefined_variables}")
        raise click.Abort()

    temp_output_file: str = ""
    output_file = f"{output_dir}/{format_resource_kind(resource_kind=resource_dict['KIND'])}.py"
    if os.path.exists(output_file):
        if overwrite:
            LOGGER.warning(f"Overwriting {output_file}")
        else:
            temp_output_file = f"{output_file[:-3]}_TEMP.py"
            LOGGER.warning(f"{output_file} already exists, using {temp_output_file}")
            output_file = temp_output_file

    if dry_run:
        Console().print(rendered)

    else:
        with open(output_file, "w") as fd:
            fd.write(rendered)

        for op in ("format", "check"):
            run_command(
                command=shlex.split(f"poetry run ruff {op} {output_file}"),
                verify_stderr=False,
                check=False,
            )

    return output_file


def parse_explain(
    api_link: str,
    output: str,
    namespaced: Optional[bool] = None,
    debug: bool = False,
    output_debug_file_path: str = "",
    debug_content: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    section_data: str = ""
    sections: List[str] = []
    resource_dict: Dict[str, Any] = {
        "BASE_CLASS": "NamespacedResource" if namespaced else "Resource",
        "API_LINK": api_link,
    }
    new_sections_words: Tuple[str, str, str] = ("KIND:", "VERSION:", "GROUP:")

    for line in output.splitlines():
        # If line is empty section is done
        if not line.strip():
            if section_data:
                sections.append(section_data)
                section_data = ""

            continue

        section_data += f"{line}\n"
        if line.startswith(new_sections_words):
            if section_data:
                sections.append(section_data)
                section_data = ""
            continue

    # Last section data from last iteration
    if section_data:
        sections.append(section_data)

    start_fields_section: str = ""

    for section in sections:
        if section.startswith(f"{FIELDS_STR}:"):
            start_fields_section = section
            continue

        key, val = section.split(":")
        resource_dict[key.strip()] = val.strip()

    kind = resource_dict["KIND"]
    keys_to_ignore = ["metadata", "kind", "apiVersion", "status"]
    resource_dict[SPEC_STR] = []
    resource_dict[FIELDS_STR] = []
    first_field_indent: int = 0
    first_field_indent_str: str = ""
    top_spec_indent: int = 0
    top_spec_indent_str: str = ""
    first_field_spec_found: bool = False
    field_spec_found: bool = False

    for field in start_fields_section.splitlines():
        if field.startswith(f"{FIELDS_STR}:"):
            continue

        start_spec_field = field.startswith(f"{first_field_indent_str}{SPEC_STR.lower()}")
        ignored_field = field.split()[0] in keys_to_ignore
        # Find first indent of spec, Needed in order to now when spec is done.
        if not first_field_indent:
            first_field_indent = len(re.findall(r" +", field)[0])
            first_field_indent_str = f"{' ' * first_field_indent}"
            if not ignored_field and not start_spec_field:
                resource_dict[FIELDS_STR].append(
                    get_arg_params(
                        field=field,
                        kind=kind,
                        debug=debug,
                        output_debug_file_path=output_debug_file_path,
                    )
                )

            continue
        else:
            if len(re.findall(r" +", field)[0]) == len(first_field_indent_str):
                if not ignored_field and not start_spec_field:
                    resource_dict[FIELDS_STR].append(
                        get_arg_params(
                            field=field,
                            kind=kind,
                            debug=debug,
                            output_debug_file_path=output_debug_file_path,
                        )
                    )

        if start_spec_field:
            first_field_spec_found = True
            field_spec_found = True
            continue

        if field_spec_found:
            if not re.findall(rf"^{first_field_indent_str}\w", field):
                if first_field_spec_found:
                    resource_dict[SPEC_STR].append(
                        get_arg_params(
                            field=field,
                            kind=kind,
                            field_under_spec=True,
                            debug=debug,
                            debug_content=debug_content,
                            output_debug_file_path=output_debug_file_path,
                        )
                    )

                    # Get top level keys inside spec indent, need to match only once.
                    top_spec_indent = len(re.findall(r" +", field)[0])
                    top_spec_indent_str = f"{' ' * top_spec_indent}"
                    first_field_spec_found = False
                    continue

                if top_spec_indent_str:
                    # Get only top level keys from inside spec
                    if re.findall(rf"^{top_spec_indent_str}\w", field):
                        resource_dict[SPEC_STR].append(
                            get_arg_params(
                                field=field,
                                kind=kind,
                                field_under_spec=True,
                                debug=debug,
                                debug_content=debug_content,
                                output_debug_file_path=output_debug_file_path,
                            )
                        )
                        continue

            else:
                break

    if not resource_dict[SPEC_STR] and not resource_dict[FIELDS_STR]:
        LOGGER.error(f"Unable to parse {kind} resource.")
        return {}

    api_group_real_name = resource_dict.get("GROUP")
    # If API Group is not present in resource, try to get it from VERSION
    if not api_group_real_name:
        version_splited = resource_dict["VERSION"].split("/")
        if len(version_splited) == 2:
            api_group_real_name = version_splited[0]

    if api_group_real_name:
        api_group_for_resource_api_group = api_group_real_name.upper().replace(".", "_")
        resource_dict["GROUP"] = api_group_for_resource_api_group
        missing_api_group_in_resource: bool = not hasattr(Resource.ApiGroup, api_group_for_resource_api_group)

        if missing_api_group_in_resource:
            LOGGER.warning(
                f"Missing API Group in Resource\n"
                f"Please add `Resource.ApiGroup.{api_group_for_resource_api_group} = {api_group_real_name}` "
                "manually into ocp_resources/resource.py under Resource class > ApiGroup class."
            )

    else:
        api_version_for_resource_api_version = resource_dict["VERSION"].upper()
        missing_api_version_in_resource: bool = not hasattr(Resource.ApiVersion, api_version_for_resource_api_version)

        if missing_api_version_in_resource:
            LOGGER.warning(
                f"Missing API Version in Resource\n"
                f"Please add `Resource.ApiVersion.{api_version_for_resource_api_version} = {resource_dict['VERSION']}` "
                "manually into ocp_resources/resource.py under Resource class > ApiGroup class."
            )

    return resource_dict


def validate_api_link_schema(value: str) -> str:
    if not value.startswith("https://"):
        raise click.BadParameter("Resource API linkn must start with https://")

    return value


def check_kind_exists(kind: str) -> bool:
    return run_command(
        command=shlex.split(f"oc explain {kind}"),
        check=False,
    )[0]


def get_user_args_from_interactive() -> Tuple[str, str]:
    kind = Prompt.ask(prompt="Enter the resource kind to generate class for")
    if not kind:
        return "", ""

    api_link = Prompt.ask(prompt="Enter the resource API link")
    if not api_link:
        return "", ""

    return kind, api_link


def class_generator(
    kind: str = "",
    api_link: str = "",
    overwrite: bool = False,
    interactive: bool = False,
    dry_run: bool = False,
    debug: bool = False,
    process_debug_file: str = "",
    generated_file_output_dir: str = "ocp_resources",
) -> str:
    """
    Generates a class for a given Kind.
    """
    debug_content: Dict[str, str] = {}
    output_debug_file_path = os.path.join(os.path.dirname(__file__), "debug", f"{kind}-debug.json")

    if process_debug_file:
        debug = False
        with open(process_debug_file) as fd:
            debug_content = json.load(fd)

        kind_data = debug_content["explain"]
        namespaced = debug_content["namespace"].strip() == "1"
        api_link = "https://debug.explain"

    else:
        if not check_cluster_available():
            LOGGER.error(
                "Cluster not available, The script needs a running cluster and admin privileges to get the explain output"
            )
            return ""

        if interactive:
            kind, api_link = get_user_args_from_interactive()

        if not kind or not api_link:
            LOGGER.error("Kind or API link not provided")
            return ""

        validate_api_link_schema(value=api_link)

        if not check_kind_exists(kind=kind):
            return ""

        explain_output = get_kind_data(kind=kind, debug=debug, output_debug_file_path=output_debug_file_path)
        if not explain_output:
            return ""

        namespaced = explain_output["namespaced"]
        kind_data = explain_output["data"]

    resource_dict = parse_explain(
        output=kind_data,
        namespaced=namespaced,
        api_link=api_link,
        debug=debug,
        output_debug_file_path=output_debug_file_path,
        debug_content=debug_content,
    )
    if not resource_dict:
        return ""

    generated_py_file = generate_resource_file_from_dict(
        resource_dict=resource_dict,
        overwrite=overwrite,
        dry_run=dry_run,
        output_dir=generated_file_output_dir,
    )

    if not dry_run:
        run_command(
            command=shlex.split(f"pre-commit run --files {generated_py_file}"),
            verify_stderr=False,
            check=False,
        )

    if debug:
        LOGGER.info(f"Debug output saved to {output_debug_file_path}")

    return generated_py_file


@click.command("Resource class generator")
@click.option(
    "-k",
    "--kind",
    type=click.STRING,
    help="The Kind to generate the class for, Needs working cluster with admin privileges",
)
@click.option(
    "-l",
    "--api-link",
    help="A link to the resource doc/api in the web",
)
@click.option(
    "-o",
    "--overwrite",
    is_flag=True,
    help="Output file overwrite existing file if passed",
)
@click.option("-d", "--debug", is_flag=True, help="Save all command output to debug file")
@click.option("-i", "--interactive", is_flag=True, help="Enable interactive mode")
@click.option("--dry-run", is_flag=True, help="Run the script without writing to file")
@click.option(
    "--debug-file",
    type=click.Path(exists=True),
    help="Run the script from debug file. (generated by -d)",
)
def main(
    kind: str,
    api_link: str,
    overwrite: bool,
    interactive: bool,
    dry_run: bool,
    debug: bool,
    debug_file: str,
):
    return class_generator(
        kind=kind,
        api_link=api_link,
        overwrite=overwrite,
        interactive=interactive,
        dry_run=dry_run,
        debug=debug,
        process_debug_file=debug_file,
    )


if __name__ == "__main__":
    main()
