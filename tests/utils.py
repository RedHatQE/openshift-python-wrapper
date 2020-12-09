import re

import jinja2
import yaml


class MissingTemplateVariables(Exception):
    def __init__(self, var, template):
        self.var = var
        self.template = template

    def __str__(self):
        return f"Missing variables {self.var} for template {self.template}"


def generate_yaml_from_template(**kwargs):
    """
    Generate JSON from yaml file_

    Keyword Args:
        name (str):
        image (str):

    Returns:
        dict: Generated from template file

    Raises:
        MissingTemplateVariables: If not all template variables exists

    Examples:
        generate_yaml_from_template(file_='path/to/file/name', name='vm-name-1')
    """
    file_ = "tests/manifests/vm.yaml"
    with open(file_, "r") as stream:
        data = stream.read()

    # Find all template variables
    template_vars = [i.split()[1] for i in re.findall(r"{{ .* }}", data)]
    for var in template_vars:
        if var not in kwargs.keys():
            raise MissingTemplateVariables(var=var, template=file_)

    template = jinja2.Template(source=data)
    out = template.render(**kwargs)
    return yaml.safe_load(stream=out)
