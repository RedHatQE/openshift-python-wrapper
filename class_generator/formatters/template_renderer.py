"""Jinja template rendering for resource generation."""

from pathlib import Path
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

    # Parse the template source to find undeclared variables
    # Get template source in a way that's compatible with different Jinja2 versions
    try:
        # Try to get source directly (newer Jinja2 versions)
        template_source = template.source
    except AttributeError:
        # Fallback: read the template file directly
        template_path = Path(template_dir) / template_name
        with open(template_path, encoding="utf-8") as f:
            template_source = f.read()

    ast = env.parse(source=template_source)
    undeclared_variables = meta.find_undeclared_variables(ast)

    # Filter out variables that are present in template_dict
    # We need to check all levels of the template_dict for nested access
    provided_variables = set(template_dict.keys())

    # Find truly undefined variables
    undefined_variables = undeclared_variables - provided_variables

    if undefined_variables:
        error_msg = f"The following variables are undefined in template '{template_name}': {undefined_variables}. Available variables: {provided_variables}"
        LOGGER.error(error_msg)
        raise ValueError(error_msg)

    # Now render the template
    rendered = template.render(template_dict)

    return rendered
