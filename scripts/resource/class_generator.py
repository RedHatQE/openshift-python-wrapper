from __future__ import annotations
import shlex
import os

from typing import Any, Dict, List, Optional, Tuple
import click
import re

from pyhelper_utils.shell import run_command
import yaml

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
    if os.system("which oc") == 0:
        return "oc"

    elif os.system("which kubectl") == 0:
        return "kubectl"

    else:
        LOGGER.error("oc or kubectl not available")
        return ""


def check_cluster_available() -> bool:
    _exec = get_oc_or_kubectl()
    if not _exec:
        return False

    return os.system(f"{_exec} version") == 0


def get_kind_data(kind: str) -> Dict[str, Any]:
    """
    Get oc/kubectl explain output for given kind and if kind is namespaced
    """
    if not check_cluster_available():
        LOGGER.error("Cluster not available")
        return {}

    explain_rc, explain_out, explain_err = run_command(command=shlex.split(f"oc explain {kind} --recursive"))
    if not explain_rc:
        LOGGER.error(f"Failed to get explain for {kind}, error: {explain_err}")
        return {}

    resource_kind = re.search(r".*?KIND:\s+(.*?)\n", explain_out)
    if not resource_kind:
        LOGGER.error(f"Failed to get resource kind from explain for {kind}")
        return {}

    _, namespace_out, _ = run_command(
        command=shlex.split(f"bash -c 'oc api-resources --namespaced | grep -w {resource_kind.group(1)} | wc -l'"),
        check=False,
    )
    if namespace_out.strip() == "1":
        return {"data": explain_out, "namespaced": True}

    return {"data": explain_out, "namespaced": False}


def format_resource_kind(resource_kind: str) -> str:
    """Convert CamelCase to snake_case"""
    return re.sub(r"(?<!^)(?<=[a-z])(?=[A-Z])", "_", resource_kind).lower().strip()


def get_field_description(kind: str, field_name: str, field_under_spec: bool) -> str:
    _, _out, _ = run_command(
        command=shlex.split(f"oc explain {kind}{'.spec' if field_under_spec else ''}.{field_name}"),
        check=False,
        verify_stderr=False,
    )
    _description = re.search(r"DESCRIPTION:\n\s*(.*)", _out, re.DOTALL)
    if _description:
        description: str = ""
        indent: int = 0
        for line in _description.group(1).strip().splitlines():
            if line.strip():
                description += f"{' ' * indent}{line}\n"
            else:
                indent = indent + 4
                description += f"{' ' * indent}{line}\n"

        return f"{description}\n"

    return "<please add description>"


def get_arg_params(field: str, kind: str, field_under_spec: bool = False, use_cluster: bool = False) -> Dict[str, Any]:
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
        "description": "<please add description>",
    }

    if use_cluster:
        _res["description"] = get_field_description(kind=kind, field_name=_orig_name, field_under_spec=field_under_spec)
    return _res


def generate_resource_file_from_dict(resource_dict: Dict[str, Any], output_dir="ocp_resources") -> str:
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
        temp_output_file = f"{output_file[:-3]}_TEMP.py"
        LOGGER.warning(f"{output_file} already exists, using {temp_output_file}")
        output_file = temp_output_file

    with open(output_file, "w") as fd:
        fd.write(rendered)

    for op in ("format", "check"):
        run_command(
            command=shlex.split(f"poetry run ruff {op} {output_file}"),
            verify_stderr=False,
        )

    return output_file


def parse_explain(
    api_link: str,
    use_cluster: bool = False,
    file: Optional[str] = "",
    output: Optional[str] = "",
    namespaced: Optional[bool] = None,
) -> Dict[str, Any]:
    section_data: str = ""
    sections: List[str] = []
    resource_dict: Dict[str, Any] = {
        "BASE_CLASS": "NamespacedResource" if namespaced else "Resource",
        "API_LINK": api_link,
    }
    new_sections_words: Tuple[str, str, str] = ("KIND:", "VERSION:", "GROUP:")

    if file:
        with open(file) as fd:
            data = fd.read()
    elif output:
        data = output

    else:
        LOGGER.error("Provide file or output")
        return {}

    for line in data.splitlines():
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
                resource_dict[FIELDS_STR].append(get_arg_params(field=field, kind=kind, use_cluster=use_cluster))

            continue
        else:
            if len(re.findall(r" +", field)[0]) == len(first_field_indent_str):
                if not ignored_field and not start_spec_field:
                    resource_dict[FIELDS_STR].append(get_arg_params(field=field, kind=kind, use_cluster=use_cluster))

        if start_spec_field:
            first_field_spec_found = True
            field_spec_found = True
            continue

        if field_spec_found:
            if not re.findall(rf"^{first_field_indent_str}\w", field):
                if first_field_spec_found:
                    resource_dict[SPEC_STR].append(
                        get_arg_params(field=field, kind=kind, field_under_spec=True, use_cluster=use_cluster)
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
                            get_arg_params(field=field, kind=kind, field_under_spec=True, use_cluster=use_cluster)
                        )
                        continue

            else:
                break

    if not resource_dict[SPEC_STR] and not resource_dict[FIELDS_STR]:
        LOGGER.error(f"Unable to parse {kind} resource.")
        return {}

    LOGGER.debug(f"\n{yaml.dump(resource_dict)}")

    if api_group_real_name := resource_dict.get("GROUP"):
        api_group_for_resource_api_group = api_group_real_name.upper().replace(".", "_")
        missing_api_group_in_resource: bool = not hasattr(Resource.ApiGroup, api_group_for_resource_api_group)

        if missing_api_group_in_resource:
            LOGGER.warning(
                f"Missing API Group in Resource\nPlease add `Resource.ApiGroup.{api_group_real_name} = {api_group_real_name}` manually into ocp_resources/resource.py under Resource class > ApiGroup class."
            )

    return resource_dict


def validate_api_link_schema(ctx: click.Context, param: click.Option | click.Parameter, value: Any) -> Any:
    if not value.startswith("https://"):
        raise click.BadParameter("Resource API linkn must start with https://")

    return value


@click.command("Resource class generator")
@click.option(
    "-f",
    "--file",
    type=click.Path(),
    help="File containing the content of: `oc explain <KIND> --recursive`",
)
@click.option(
    "-k",
    "--kind",
    type=click.STRING,
    help="The Kind to generate the class for, Needs working cluster with admin privileges",
)
@click.option(
    "-ns",
    "--namespaced",
    is_flag=True,
    help="""
    \b
    Indicate if the resource is nemaspaced.
        Get it by: `oc api-resources --namespaced | grep -w <KIND>`
    """,
)
@click.option(
    "-l",
    "--api-link",
    required=True,
    type=click.UNPROCESSED,
    callback=validate_api_link_schema,
    help="A link to the resource doc/api in the web",
)
@click.option("-v", "--verbose", is_flag=True, help="Enable debug logs")
def main(file: str, kind: str, namespaced: bool, api_link: str, verbose: bool) -> None:
    """
    Generates a class for a given Kind.
    Either pass --file or --kind (When passing --kind a working cluster is required)
    """
    kind_data: str = ""
    LOGGER.setLevel("DEBUG" if verbose else "INFO")
    if file and kind:
        LOGGER.error("Please pass either --file or --kind")
        return

    if kind:
        if namespaced:
            LOGGER.warning("`--namespaced` is ignored when `--kind` is provided.")

        explain_output = get_kind_data(kind=kind)
        if not explain_output:
            LOGGER.error("Kind not found")
            return

        namespaced = explain_output["namespaced"]
        kind_data = explain_output["data"]

    resource_dict = parse_explain(
        file=file, output=kind_data, namespaced=namespaced, api_link=api_link, use_cluster=bool(kind)
    )
    if not resource_dict:
        return

    generate_resource_file_from_dict(resource_dict=resource_dict)
    run_command(command=shlex.split("pre-commit run --all-files"), verify_stderr=False, check=False)


if __name__ == "__main__":
    main()
