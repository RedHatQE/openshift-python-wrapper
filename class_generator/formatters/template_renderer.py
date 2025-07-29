"""Jinja template rendering for resource generation."""

import sys
from typing import Any

from jinja2 import DebugUndefined, Environment, FileSystemLoader, meta
from simple_logger.logger import get_logger

LOGGER = get_logger(name=__name__)


def render_jinja_template(template_dict: dict[Any, Any], template_dir: str, template_name: str) -> str:
    """
    Render a Jinja template with the provided context.

    Args:
        template_dict: Dictionary of variables to pass to the template
        template_dir: Directory containing the template
        template_name: Name of the template file

    Returns:
        Rendered template as string
    """
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
