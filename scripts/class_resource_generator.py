from __future__ import annotations
from typing import Any, Dict, List, Tuple
import click
import re

TYPE_MAPPING: Dict[str, str] = {
    "<integer>": "int",
    "<Object>": "Dict[Any, Any]",
    "<[]Object>": "List[Any]",
    "<string>": "str",
    "<map[string]string>": "Dict[Any, Any]",
    "<boolean>": "bool",
}


def name_and_type_from_field(field: str) -> Tuple[str, str, bool]:
    splited_field = field.split()
    _name, _type = splited_field[0], splited_field[1]
    name = re.sub(r"(?<!^)(?=[A-Z])", "_", _name).lower().strip()
    type_ = _type.strip()
    required = "-required-" in splited_field
    type_from_dict = TYPE_MAPPING.get(type_, "Dict[Any, Any]")

    if not required:
        if type_from_dict == "Dict[Any, Any]":
            type_from_dict = "Option[Dict[str, Any]] = None"

        if type_from_dict == "List[Any]":
            type_from_dict = "Option[List[Any]] = None"

        if type_from_dict == "str":
            type_from_dict = "Option[str] = ''"

        if type_from_dict == "bool":
            type_from_dict = "Option[bool] = None"

        if type_from_dict == "int":
            type_from_dict = "Option[int] = None"

    return name, f"{name}: {type_from_dict}", required


def generate_resource_file_from_dict(resource_dict: Dict[str, Any]) -> None:
    pass


def resource_from_explain_file(file: str, namespaced: bool, api_link: str) -> Dict[str, Any]:
    section_data: str = ""
    sections: List[str] = []
    resource_dict: Dict[str, Any] = {}
    resource_dict["BASE_CLASS"] = "NamespacedResource" if namespaced else "Resource"
    resource_dict["API_LINK"] = api_link
    new_sections_words: Tuple[str, str, str] = ("KIND:", "VERSION:", "GROUP:")

    with open(file) as fd:
        data = fd.read()

    for line in data.splitlines():
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
                    resource_dict["SPEC"].append(name_and_type_from_field(field=field))
                    top_spec_indent = len(re.findall(r" +", field)[0])
                    top_spec_indent_str = f"{' ' * top_spec_indent}"
                    first_field_spec_found = False
                    continue

                if top_spec_indent_str:
                    if re.findall(rf"^{top_spec_indent_str}\w", field):
                        resource_dict["SPEC"].append(name_and_type_from_field(field=field))
                        continue

            else:
                break

    resource_dict["SPEC"].sort(key=lambda x: not x[-1])

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
    Indicate if the resource is nemaspaced or not.
        Get it by:  `oc api-resources --namespaced | grep <KIND>`
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
def main(file, namespaced, api_link):
    resource_dict = resource_from_explain_file(file=file, namespaced=namespaced, api_link=api_link)
    generate_resource_file_from_dict(resource_dict=resource_dict)


if __name__ == "__main__":
    main()
