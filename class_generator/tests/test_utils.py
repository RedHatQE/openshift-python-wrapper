"""Tests for utils module."""

import tempfile
from pathlib import Path

import pytest

from class_generator.utils import (
    ResourceScanner,
    get_latest_version,
    sanitize_python_name,
)


class TestSanitizePythonName:
    """Test cases for sanitize_python_name function."""

    def test_sanitize_reserved_keywords(self):
        """Test sanitizing Python reserved keywords."""
        assert sanitize_python_name("class") == ("class_", "class")
        assert sanitize_python_name("for") == ("for_", "for")
        assert sanitize_python_name("import") == ("import_", "import")
        assert sanitize_python_name("if") == ("if_", "if")

    def test_sanitize_normal_names(self):
        """Test that normal names are not changed."""
        assert sanitize_python_name("my_variable") == ("my_variable", "my_variable")
        assert sanitize_python_name("data") == ("data", "data")
        assert sanitize_python_name("resource_name") == ("resource_name", "resource_name")

    def test_sanitize_empty_string(self):
        """Test sanitizing empty string."""
        assert sanitize_python_name("") == ("", "")


class TestGetLatestVersion:
    """Test cases for get_latest_version function."""

    def test_get_latest_version_simple(self):
        """Test getting latest version from simple version list."""
        versions = ["v1alpha1", "v1beta1", "v1"]
        assert get_latest_version(versions) == "v1"

    def test_get_latest_version_with_groups(self):
        """Test getting latest version with API groups."""
        versions = ["apps/v1", "apps/v1beta1", "apps/v1beta2"]
        assert get_latest_version(versions) == "apps/v1"

    def test_get_latest_version_mixed(self):
        """Test getting latest version from mixed formats."""
        versions = ["v1alpha1", "v1beta2", "v1beta1", "v2", "v1"]
        assert get_latest_version(versions) == "v2"

    def test_get_latest_version_empty_list(self):
        """Test getting latest version from empty list."""
        assert get_latest_version([]) == ""

    def test_get_latest_version_single_item(self):
        """Test getting latest version from single item list."""
        assert get_latest_version(["v1"]) == "v1"

    def test_get_latest_version_unknown_versions(self):
        """Test getting latest version with unknown version formats."""
        versions = ["v3custom", "v1"]
        # Should still pick v1 as it's a known version
        assert get_latest_version(versions) == "v1"

    def test_get_latest_version_all_unknown(self):
        """Test getting latest version when all versions are unknown."""
        versions = ["custom1", "custom2", "custom3"]
        # Should return first item when all are unknown
        assert get_latest_version(versions) == "custom1"


class TestResourceScanner:
    """Test cases for ResourceScanner class."""

    @pytest.fixture
    def temp_ocp_resources_dir(self):
        """Create a temporary directory for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    def test_scan_resources_with_valid_files(self, temp_ocp_resources_dir):
        """Test scanning resources with valid resource files."""
        # Create a valid resource file
        resource_content = '''# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any
from ocp_resources.resource import NamespacedResource, MissingRequiredArgumentError


class Pod(NamespacedResource):
    """Pod resource."""

    api_version = NamespacedResource.ApiVersion.V1

    def __init__(self, containers=None, name=None, namespace=None, **kwargs):
        super().__init__(name=name, namespace=namespace, **kwargs)
        self.containers = containers

    def to_dict(self):
        res = super().to_dict()
        if not self.containers:
            raise MissingRequiredArgumentError(argument="self.containers")
        return res
'''

        resource_file = temp_ocp_resources_dir / "pod.py"
        resource_file.write_text(data=resource_content)

        # Create __init__.py (should be excluded)
        init_file = temp_ocp_resources_dir / "__init__.py"
        init_file.write_text(data="")

        scanner = ResourceScanner(ocp_resources_path=str(temp_ocp_resources_dir))
        resources = scanner.scan_resources()

        assert len(resources) == 1
        assert resources[0].name == "Pod"
        assert resources[0].base_class == "NamespacedResource"
        assert resources[0].api_version == "v1"
        assert resources[0].has_containers is True
        assert "containers" in resources[0].required_params
        assert resources[0].is_ephemeral is False

    def test_scan_resources_ignores_non_generated_files(self, temp_ocp_resources_dir):
        """Test that scanner ignores files without the generated marker."""
        # Create a file without the generated marker
        resource_content = '''from ocp_resources.resource import Resource


class CustomResource(Resource):
    """Custom resource."""
    pass
'''

        resource_file = temp_ocp_resources_dir / "custom.py"
        resource_file.write_text(data=resource_content)

        scanner = ResourceScanner(ocp_resources_path=str(temp_ocp_resources_dir))
        resources = scanner.scan_resources()

        assert len(resources) == 0

    def test_extract_resource_info_with_base_resource(self, temp_ocp_resources_dir):
        """Test extracting info from a Resource-based class."""
        resource_content = '''# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from ocp_resources.resource import Resource


class ClusterResource(Resource):
    """Cluster-scoped resource."""

    api_group = Resource.ApiGroup.CLUSTER_EXAMPLE_COM
    api_version = Resource.ApiVersion.V1BETA1

    def __init__(self, spec=None, **kwargs):
        super().__init__(**kwargs)
        self.spec = spec
'''

        resource_file = temp_ocp_resources_dir / "cluster_resource.py"
        resource_file.write_text(data=resource_content)

        scanner = ResourceScanner(ocp_resources_path=str(temp_ocp_resources_dir))
        resources = scanner.scan_resources()

        assert len(resources) == 1
        assert resources[0].name == "ClusterResource"
        assert resources[0].base_class == "Resource"
        assert resources[0].api_group == "cluster.example.com"
        assert resources[0].api_version == "v1beta1"
        assert "spec" in resources[0].optional_params

    def test_extract_resource_info_ephemeral_resource(self, temp_ocp_resources_dir):
        """Test extracting info for ephemeral resources like ProjectRequest."""
        resource_content = '''# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from ocp_resources.resource import Resource


class ProjectRequest(Resource):
    """ProjectRequest creates a Project."""

    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)
'''

        resource_file = temp_ocp_resources_dir / "project_request.py"
        resource_file.write_text(data=resource_content)

        scanner = ResourceScanner(ocp_resources_path=str(temp_ocp_resources_dir))
        resources = scanner.scan_resources()

        assert len(resources) == 1
        assert resources[0].name == "ProjectRequest"
        assert resources[0].is_ephemeral is True
        assert resources[0].actual_resource_type == "Project"

    def test_analyze_init_with_defaults(self, temp_ocp_resources_dir):
        """Test analyzing __init__ method with default parameters."""
        resource_content = '''# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from ocp_resources.resource import NamespacedResource


class Deployment(NamespacedResource):
    """Deployment resource."""

    def __init__(self, name, namespace, replicas=1, strategy=None, **kwargs):
        super().__init__(name=name, namespace=namespace, **kwargs)
        self.replicas = replicas
        self.strategy = strategy
'''

        resource_file = temp_ocp_resources_dir / "deployment.py"
        resource_file.write_text(data=resource_content)

        scanner = ResourceScanner(ocp_resources_path=str(temp_ocp_resources_dir))
        resources = scanner.scan_resources()

        assert len(resources) == 1
        assert "name" in resources[0].required_params
        assert "namespace" in resources[0].required_params
        assert "replicas" in resources[0].optional_params
        assert "strategy" in resources[0].optional_params

    def test_analyze_to_dict_required_params(self, temp_ocp_resources_dir):
        """Test analyzing to_dict method to find truly required parameters."""
        resource_content = '''# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from ocp_resources.resource import NamespacedResource, MissingRequiredArgumentError


class Service(NamespacedResource):
    """Service resource."""

    def __init__(self, name=None, namespace=None, selector=None, ports=None, **kwargs):
        super().__init__(name=name, namespace=namespace, **kwargs)
        self.selector = selector
        self.ports = ports

    def to_dict(self):
        res = super().to_dict()
        if not self.selector:
            raise MissingRequiredArgumentError(argument="self.selector")
        if not self.ports:
            raise MissingRequiredArgumentError(argument="self.ports")
        return res
'''

        resource_file = temp_ocp_resources_dir / "service.py"
        resource_file.write_text(data=resource_content)

        scanner = ResourceScanner(ocp_resources_path=str(temp_ocp_resources_dir))
        resources = scanner.scan_resources()

        assert len(resources) == 1
        # to_dict overrides the required params
        assert "selector" in resources[0].required_params
        assert "ports" in resources[0].required_params

    def test_extract_api_info_with_enum_style(self, temp_ocp_resources_dir):
        """Test extracting API info using enum-style attributes."""
        resource_content = '''# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from ocp_resources.resource import NamespacedResource


class Ingress(NamespacedResource):
    """Ingress resource."""

    api_group = NamespacedResource.ApiGroup.NETWORKING_K8S_IO
    api_version = NamespacedResource.ApiVersion.V1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
'''

        resource_file = temp_ocp_resources_dir / "ingress.py"
        resource_file.write_text(data=resource_content)

        scanner = ResourceScanner(ocp_resources_path=str(temp_ocp_resources_dir))
        resources = scanner.scan_resources()

        assert len(resources) == 1
        assert resources[0].api_group == "networking.k8s.io"
        assert resources[0].api_version == "v1"

    def test_scan_empty_directory(self, temp_ocp_resources_dir):
        """Test scanning an empty directory."""
        scanner = ResourceScanner(ocp_resources_path=str(temp_ocp_resources_dir))
        resources = scanner.scan_resources()

        assert len(resources) == 0

    def test_scan_resources_sorted_by_name(self, temp_ocp_resources_dir):
        """Test that resources are returned sorted by name."""
        # Create multiple resource files
        for name in ["zebra", "alpha", "beta"]:
            content = f"""# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from ocp_resources.resource import Resource


class {name.capitalize()}(Resource):
    pass
"""
            resource_file = temp_ocp_resources_dir / f"{name}.py"
            resource_file.write_text(data=content)

        scanner = ResourceScanner(ocp_resources_path=str(temp_ocp_resources_dir))
        resources = scanner.scan_resources()

        assert len(resources) == 3
        assert resources[0].name == "Alpha"
        assert resources[1].name == "Beta"
        assert resources[2].name == "Zebra"
