from __future__ import annotations
import shlex
import os

from typing import Any, Dict, List, Tuple
import click
import re

from pyhelper_utils.shell import run_command
import yaml

from ocp_resources.resource import Resource

from jinja2 import DebugUndefined, Environment, FileSystemLoader, meta
from simple_logger.logger import get_logger

TYPE_MAPPING: Dict[str, str] = {
    "<integer>": "int",
    "<Object>": "Dict[Any, Any]",
    "<[]Object>": "List[Any]",
    "<string>": "str",
    "<map[string]string>": "Dict[Any, Any]",
    "<boolean>": "bool",
}
LOGGER = get_logger(name="class_generator")


def format_resource_kind(resource_kind: str) -> str:
    """Convert CamelCase to snake_case"""
    return re.sub(r"(?<!^)(?<=[a-z])(?=[A-Z])", "_", resource_kind).lower().strip()


def get_spec_arg_params(field: str) -> Tuple[str, str, bool, str]:
    splited_field = field.split()
    _name, _type = splited_field[0], splited_field[1]

    name = format_resource_kind(resource_kind=_name)
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

    return (
        name,
        f"{name}: {type_from_dict_for_init}",
        required,
        type_from_dict,
    )


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


def parse_explain_file(file: str, namespaced: bool, api_link: str) -> Dict[str, Any]:
    section_data: str = ""
    sections: List[str] = []
    resource_dict: Dict[str, Any] = {
        "BASE_CLASS": "NamespacedResource" if namespaced else "Resource",
        "API_LINK": api_link,
    }
    new_sections_words: Tuple[str, str, str] = ("KIND:", "VERSION:", "GROUP:")

    with open(file) as fd:
        data = fd.read()

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
        if section.startswith("FIELDS:"):
            start_fields_section = section
            continue

        key, val = section.split(":")
        resource_dict[key.strip()] = val.strip()

    resource_dict["SPEC"] = []
    first_field_indent: int = 0
    first_field_indent_str: str = ""
    top_spec_indent: int = 0
    top_spec_indent_str: str = ""
    first_field_spec_found: bool = False
    field_spec_found: bool = False

    for field in start_fields_section.splitlines():
        if field.startswith("FIELDS:"):
            continue

        # Find first indent of spec, Needed in order to now when spec is done.
        if not first_field_indent:
            first_field_indent = len(re.findall(r" +", field)[0])
            first_field_indent_str = f"{' ' * first_field_indent}"
            continue

        if field.startswith(f"{first_field_indent_str}spec"):
            first_field_spec_found = True
            field_spec_found = True
            continue

        if field_spec_found:
            if not re.findall(rf"^{first_field_indent_str}\w", field):
                if first_field_spec_found:
                    resource_dict["SPEC"].append(get_spec_arg_params(field=field))

                    # Get top level keys inside spec indent, need to match only once.
                    top_spec_indent = len(re.findall(r" +", field)[0])
                    top_spec_indent_str = f"{' ' * top_spec_indent}"
                    first_field_spec_found = False
                    continue

                if top_spec_indent_str:
                    # Get only top level keys from inside spec
                    if re.findall(rf"^{top_spec_indent_str}\w", field):
                        resource_dict["SPEC"].append(get_spec_arg_params(field=field))
                        continue

            else:
                break

    resource_dict["SPEC"].sort(key=lambda x: not x[-1])
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
    type=click.Path(exists=True),
    help="File containing the content of: `oc explain <KIND> --recursive`",
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
def main(file, namespaced, api_link, verbose):
    LOGGER.setLevel("DEBUG" if verbose else "INFO")

    resource_dict = parse_explain_file(file=file, namespaced=namespaced, api_link=api_link)
    generate_resource_file_from_dict(resource_dict=resource_dict)
    run_command(command=shlex.split("pre-commit run --all-files"), verify_stderr=False, check=False)


if __name__ == "__main__":
    main()
