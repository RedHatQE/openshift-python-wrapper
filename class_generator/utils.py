"""Utilities for class generator."""

import ast
from collections.abc import Callable, Iterable
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, TypeVar

from simple_logger.logger import get_logger

from class_generator.constants import PYTHON_KEYWORD_MAPPINGS, VERSION_PRIORITY

LOGGER = get_logger(name=__name__)

# Type variables for generic parallel execution
T = TypeVar("T")  # Input task type
R = TypeVar("R")  # Result type


def execute_parallel_tasks(
    tasks: Iterable[T],
    task_func: Callable[[T], R],
    max_workers: int | None = None,
    task_name: str = "task",
    result_processor: Callable[[T, R], Any] | None = None,
    error_handler: Callable[[T, Exception], Any] | None = None,
) -> list[tuple[T, R | Exception]]:
    """
    Execute tasks in parallel using ThreadPoolExecutor.

    This generic helper eliminates code duplication for parallel execution patterns
    throughout the class generator codebase.

    Args:
        tasks: Iterable of tasks to execute
        task_func: Function to execute for each task
        max_workers: Maximum number of worker threads (defaults to min(10, len(tasks)))
        task_name: Name for logging purposes
        result_processor: Optional function to process successful results
        error_handler: Optional function to handle exceptions

    Returns:
        List of tuples containing (task, result_or_exception) for each task

    Example:
        # Simple usage
        results = execute_parallel_tasks(
            tasks=resources,
            task_func=regenerate_single_resource,
            task_name="regeneration"
        )

        # With custom processing
        def process_result(resource, result):
            kind, success, error = result
            if success:
                LOGGER.info(f"Success: {kind}")
            else:
                LOGGER.error(f"Failed: {kind} - {error}")

        results = execute_parallel_tasks(
            tasks=resources,
            task_func=regenerate_single_resource,
            result_processor=process_result,
            task_name="regeneration"
        )
    """
    task_list = list(tasks)
    if not task_list:
        return []

    # Default max_workers to min(10, len(tasks))
    if max_workers is None:
        max_workers = min(10, len(task_list))

    results: list[tuple[T, R | Exception]] = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks and create mapping from future to task
        future_to_task: dict[Any, T] = {executor.submit(task_func, task): task for task in task_list}

        # Process results as they complete
        for future in as_completed(future_to_task):
            task = future_to_task[future]
            try:
                result = future.result()
                results.append((task, result))

                # Optional result processing
                if result_processor:
                    result_processor(task, result)

            except Exception as exc:
                results.append((task, exc))

                # Optional error handling
                if error_handler:
                    error_handler(task, exc)
                else:
                    LOGGER.exception(f"Failed to execute {task_name} for {task}: {exc}")

    return results


def execute_parallel_with_mapping(
    task_mapping: dict[T, Any],
    task_func: Callable[[T], R],
    max_workers: int | None = None,
    task_name: str = "task",
    result_processor: Callable[[T, R], Any] | None = None,
    error_handler: Callable[[T, Exception], Any] | None = None,
) -> dict[T, R | Exception]:
    """
    Execute tasks in parallel where each task has associated metadata.

    This is useful when you need to maintain a mapping between tasks and their
    associated data (like API paths to schema info).

    Args:
        task_mapping: Dictionary mapping tasks to their associated data
        task_func: Function to execute for each task (receives only the task)
        max_workers: Maximum number of worker threads
        task_name: Name for logging purposes
        result_processor: Optional function to process successful results.
                         Called with (task, result) on success. Any exceptions
                         from this function are logged but do not affect the
                         overall execution.
        error_handler: Optional function to handle task exceptions.
                      Called with (task, exception) on failure. Any exceptions
                      from this function are logged but do not affect the
                      overall execution.

    Returns:
        Dictionary mapping tasks to their results or exceptions

    Example:
        # API fetching pattern
        path_to_info = {"/api/v1": {...}, "/apis/apps/v1": {...}}
        results = execute_parallel_with_mapping(
            task_mapping=path_to_info,
            task_func=lambda path: fetch_api_group(path, path_to_info[path]),
            task_name="API fetching"
        )

        # With custom callbacks
        def log_success(task, result):
            LOGGER.info(f"Successfully processed {task}")

        def handle_error(task, error):
            LOGGER.warning(f"Task {task} failed: {error}")

        results = execute_parallel_with_mapping(
            task_mapping=path_to_info,
            task_func=lambda path: fetch_api_group(path, path_to_info[path]),
            result_processor=log_success,
            error_handler=handle_error,
            task_name="API fetching"
        )
    """
    if not task_mapping:
        return {}

    # Default max_workers to min(10, len(task_mapping))
    if max_workers is None:
        max_workers = min(10, len(task_mapping))

    results: dict[T, R | Exception] = {}

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_task: dict[Any, T] = {executor.submit(task_func, task): task for task in task_mapping.keys()}

        # Process results as they complete
        for future in as_completed(future_to_task):
            task = future_to_task[future]
            try:
                result = future.result()
                results[task] = result

                # Optional result processing
                if result_processor:
                    try:
                        result_processor(task, result)
                    except Exception as processor_exc:
                        LOGGER.exception(f"Result processor failed for {task}: {processor_exc}")

            except Exception as exc:
                results[task] = exc
                LOGGER.exception(f"Failed to execute {task_name} for {task}: {exc}")

                # Optional error handling
                if error_handler:
                    try:
                        error_handler(task, exc)
                    except Exception as handler_exc:
                        LOGGER.exception(f"Error handler failed for {task}: {handler_exc}")

    return results


def sanitize_python_name(name: str) -> tuple[str, str]:
    """Sanitize Python reserved keywords by appending underscore."""
    if name in PYTHON_KEYWORD_MAPPINGS:
        return PYTHON_KEYWORD_MAPPINGS[name], name
    return name, name


def get_latest_version(versions: list[str]) -> str:
    """
    Get the latest version from a list of Kubernetes API versions.

    Version precedence (from newest to oldest):
    - v2 > v1 > v1beta2 > v1beta1 > v1alpha2 > v1alpha1
    """
    if not versions:
        return ""

    # Sort versions by priority using imported constant
    sorted_versions = sorted(versions, key=lambda v: VERSION_PRIORITY.get(v.split("/")[-1], 0), reverse=True)

    return sorted_versions[0] if sorted_versions else versions[0]


@dataclass
class ResourceInfo:
    """Information about a discovered resource class"""

    name: str  # Class name (e.g., "Pod", "Namespace")
    file_path: str  # Path to the resource file
    base_class: str  # "Resource" or "NamespacedResource"
    api_version: str | None = None
    api_group: str | None = None
    required_params: list[str] = field(default_factory=list)
    optional_params: list[str] = field(default_factory=list)
    has_containers: bool = False
    is_ephemeral: bool = False  # True if resource is ephemeral (e.g. ProjectRequest)
    actual_resource_type: str | None = None  # The actual resource type created (e.g. "Project")


class ResourceScanner:
    """Scans ocp_resources directory to discover resource classes"""

    def __init__(self, ocp_resources_path: str = "ocp_resources"):
        self.ocp_resources_path = Path(ocp_resources_path)
        self.exclude_files = {"__init__.py", "resource.py", "exceptions.py", "utils.py"}

    def scan_resources(self) -> list[ResourceInfo]:
        """Scan ocp_resources directory and extract all resource classes"""
        resources = []

        for py_file in self.ocp_resources_path.glob("*.py"):
            if py_file.name in self.exclude_files:
                continue

            try:
                resource_info = self._analyze_resource_file(py_file)
                if resource_info:
                    resources.append(resource_info)
            except Exception as e:
                LOGGER.warning(f"Failed to analyze {py_file}: {e}")

        return sorted(resources, key=lambda r: r.name)

    def _analyze_resource_file(self, file_path: Path) -> ResourceInfo | None:
        """Analyze a single resource file to extract class information"""
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        # Only consider resources with the generated marker comment
        if (
            "# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md"
            not in content
        ):
            return None

        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            LOGGER.error(f"Syntax error in {file_path}: {e}")
            return None

        # Find resource classes
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Check if it inherits from Resource or NamespacedResource
                base_classes = []
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        base_classes.append(base.id)
                    elif isinstance(base, ast.Attribute):
                        base_classes.append(base.attr)

                if "Resource" in base_classes or "NamespacedResource" in base_classes:
                    return self._extract_resource_info(node, file_path, content)

        return None

    def _extract_resource_info(self, class_node: ast.ClassDef, file_path: Path, content: str) -> ResourceInfo:
        """Extract detailed information from a resource class"""
        name = class_node.name
        # Determine base class type
        base_class = "Resource"
        for base in class_node.bases:
            if isinstance(base, ast.Name) and base.id == "NamespacedResource":
                base_class = "NamespacedResource"
                break
            if isinstance(base, ast.Attribute) and base.attr == "NamespacedResource":
                base_class = "NamespacedResource"
                break

        # Analyze __init__ method for parameters
        required_params, optional_params, has_containers = self._analyze_init_method(class_node)

        # Analyze to_dict method for truly required parameters (those that raise MissingRequiredArgumentError)
        truly_required_params = self._analyze_to_dict_method(class_node)

        # Override required_params with what's actually required in to_dict()
        if truly_required_params:
            required_params = truly_required_params

        # Extract API version and group from class attributes or content
        api_version, api_group = self._extract_api_info(class_node, content)

        # Detect ephemeral resources
        is_ephemeral, actual_resource_type = self._handle_ephemeral_resource(name)

        return ResourceInfo(
            name=name,
            file_path=str(file_path),
            base_class=base_class,
            api_version=api_version,
            api_group=api_group,
            required_params=required_params,
            optional_params=optional_params,
            has_containers=has_containers,
            is_ephemeral=is_ephemeral,
            actual_resource_type=actual_resource_type,
        )

    def _analyze_init_method(self, class_node: ast.ClassDef) -> tuple[list[str], list[str], bool]:
        """Analyze __init__ method to find required and optional parameters"""
        required_params = []
        optional_params = []
        has_containers = False

        for node in class_node.body:
            if isinstance(node, ast.FunctionDef) and node.name == "__init__":
                # Skip 'self' and '**kwargs'
                for arg in node.args.args[1:]:
                    if arg.arg == "kwargs":
                        continue
                    param_name = arg.arg

                    # Check if parameter has default value by looking at defaults
                    # In AST, defaults align with the end of args list
                    defaults_start_idx = len(node.args.args) - len(node.args.defaults)
                    arg_idx = node.args.args.index(arg)

                    if arg_idx >= defaults_start_idx:
                        optional_params.append(param_name)
                    else:
                        required_params.append(param_name)

                    if param_name == "containers":
                        has_containers = True

        return required_params, optional_params, has_containers

    def _analyze_to_dict_method(self, class_node: ast.ClassDef) -> list[str]:
        """Analyze to_dict method to find truly required parameters"""
        truly_required = []

        for node in class_node.body:
            if isinstance(node, ast.FunctionDef) and node.name == "to_dict":
                # Look for MissingRequiredArgumentError raises
                for stmt in ast.walk(node):
                    if isinstance(stmt, ast.Raise):
                        # Check if raising MissingRequiredArgumentError
                        if isinstance(stmt.exc, ast.Call):
                            if (
                                isinstance(stmt.exc.func, ast.Name)
                                and stmt.exc.func.id == "MissingRequiredArgumentError"
                            ):
                                # Extract the parameter name from the argument
                                for keyword in stmt.exc.keywords:
                                    if keyword.arg == "argument":
                                        # Handle string format like "self.param_name"
                                        if isinstance(keyword.value, ast.Constant):
                                            param = keyword.value.value
                                            if isinstance(param, str) and param.startswith("self."):
                                                param = param[5:]  # Remove "self."
                                            if isinstance(param, str):
                                                truly_required.append(param)

        return truly_required

    def _extract_api_info(self, class_node: ast.ClassDef, _content: str) -> tuple[str | None, str | None]:
        """Extract API version and group from class attributes"""
        api_version = None
        api_group = None

        # Look for api_version or api_group class attributes
        for node in class_node.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        if target.id == "api_version" and isinstance(node.value, ast.Attribute):
                            # Extract version like Resource.ApiVersion.V1
                            if isinstance(node.value.attr, str):
                                api_version = node.value.attr.lower()
                        elif target.id == "api_group" and isinstance(node.value, ast.Attribute):
                            # Extract group like NamespacedResource.ApiGroup.APPS
                            if isinstance(node.value.attr, str):
                                api_group = node.value.attr.lower().replace("_", ".")

        return api_version, api_group

    def _handle_ephemeral_resource(self, name: str) -> tuple[bool, str | None]:
        """Check if resource is ephemeral and get actual resource type"""
        # Simple mapping for known ephemeral resources
        ephemeral_resources = {
            "ProjectRequest": "Project",
        }

        if name in ephemeral_resources:
            return True, ephemeral_resources[name]

        return False, None
