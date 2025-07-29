"""Tests for batch regeneration functionality."""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from class_generator.utils import ResourceInfo
from class_generator.core.discovery import discover_generated_resources


class TestResourceDiscovery:
    """Test resource discovery functionality."""

    @pytest.fixture
    def temp_resources_dir(self):
        """Create a temporary directory structure mimicking ocp_resources."""
        with tempfile.TemporaryDirectory() as tmpdir:
            resources_dir = Path(tmpdir) / "ocp_resources"
            resources_dir.mkdir()
            yield resources_dir

    def create_generated_file(self, path: Path, class_name: str, with_user_code: bool = False) -> None:
        """Helper to create a generated resource file."""
        content = f'''# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any
from ocp_resources.resource import NamespacedResource


class {class_name}(NamespacedResource):
    """Test resource class."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    # End of generated code
'''
        if with_user_code:
            content += '''
    def custom_method(self):
        """User added method."""
        return "custom"
'''
        path.write_text(content)

    def create_non_generated_file(self, path: Path) -> None:
        """Helper to create a non-generated resource file."""
        content = '''from ocp_resources.resource import Resource


class ManualResource(Resource):
    """Manual resource without generated marker."""
    pass
'''
        path.write_text(content)

    def create_malformed_file(self, path: Path) -> None:
        """Helper to create a malformed Python file."""
        content = """# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

class BrokenSyntax(
    # Missing closing parenthesis
"""
        path.write_text(content)

    def test_discover_finds_generated_files(self, temp_resources_dir, monkeypatch):
        """Test discovery finds all generated resource files."""
        # Create test files
        self.create_generated_file(temp_resources_dir / "pod.py", "Pod")
        self.create_generated_file(temp_resources_dir / "deployment.py", "Deployment")
        self.create_non_generated_file(temp_resources_dir / "utils.py")

        # Mock ResourceScanner to use our temp directory
        mock_scanner = MagicMock()
        mock_scanner.scan_resources.return_value = [
            ResourceInfo(name="Pod", file_path=str(temp_resources_dir / "pod.py"), base_class="NamespacedResource"),
            ResourceInfo(
                name="Deployment", file_path=str(temp_resources_dir / "deployment.py"), base_class="NamespacedResource"
            ),
        ]

        with patch("class_generator.core.discovery.ResourceScanner", return_value=mock_scanner):
            # Discover resources
            resources = discover_generated_resources()

        # Verify results
        assert len(resources) == 2
        kinds = [r["kind"] for r in resources]
        assert "Pod" in kinds
        assert "Deployment" in kinds

    def test_discover_ignores_non_generated_files(self, temp_resources_dir, monkeypatch):
        """Test discovery ignores files without the generated marker."""
        # Create mixed files
        self.create_generated_file(temp_resources_dir / "pod.py", "Pod")
        self.create_non_generated_file(temp_resources_dir / "custom.py")

        # Mock ResourceScanner to return only generated file
        mock_scanner = MagicMock()
        mock_scanner.scan_resources.return_value = [
            ResourceInfo(name="Pod", file_path=str(temp_resources_dir / "pod.py"), base_class="NamespacedResource"),
        ]

        with patch("class_generator.core.discovery.ResourceScanner", return_value=mock_scanner):
            # Discover resources
            resources = discover_generated_resources()

        # Verify only generated file is found
        assert len(resources) == 1
        assert resources[0]["kind"] == "Pod"

    def test_discover_extracts_correct_info(self, temp_resources_dir, monkeypatch):
        """Test discovery extracts all required information."""
        # Create a test file
        test_file = temp_resources_dir / "virtual_machine.py"
        self.create_generated_file(test_file, "VirtualMachine", with_user_code=True)

        # Mock ResourceScanner
        mock_scanner = MagicMock()
        mock_scanner.scan_resources.return_value = [
            ResourceInfo(name="VirtualMachine", file_path=str(test_file), base_class="NamespacedResource"),
        ]

        with patch("class_generator.core.discovery.ResourceScanner", return_value=mock_scanner):
            # Discover resources
            resources = discover_generated_resources()

        # Verify extracted information
        assert len(resources) == 1
        resource = resources[0]
        assert resource["kind"] == "VirtualMachine"
        assert resource["path"] == str(test_file)
        assert resource["filename"] == "virtual_machine"
        assert resource["has_user_code"] is True

    def test_discover_handles_malformed_files(self, temp_resources_dir, monkeypatch, caplog):
        """Test discovery handles files with syntax errors gracefully."""
        # Create files including a malformed one
        self.create_generated_file(temp_resources_dir / "pod.py", "Pod")
        self.create_malformed_file(temp_resources_dir / "broken.py")

        # Mock ResourceScanner to only return valid file
        mock_scanner = MagicMock()
        mock_scanner.scan_resources.return_value = [
            ResourceInfo(name="Pod", file_path=str(temp_resources_dir / "pod.py"), base_class="NamespacedResource"),
        ]

        with patch("class_generator.core.discovery.ResourceScanner", return_value=mock_scanner):
            # Discover resources
            resources = discover_generated_resources()

        # Verify only valid file is found
        assert len(resources) == 1
        assert resources[0]["kind"] == "Pod"

    def test_discover_skips_special_files(self, temp_resources_dir, monkeypatch):
        """Test discovery skips __init__.py, resource.py, and exceptions.py."""
        # Create files that should be skipped
        (temp_resources_dir / "__init__.py").write_text("# Init file")
        (temp_resources_dir / "resource.py").write_text("# Base resource")
        (temp_resources_dir / "exceptions.py").write_text("# Exceptions")
        self.create_generated_file(temp_resources_dir / "pod.py", "Pod")

        # Mock ResourceScanner - it should skip special files
        mock_scanner = MagicMock()
        mock_scanner.scan_resources.return_value = [
            ResourceInfo(name="Pod", file_path=str(temp_resources_dir / "pod.py"), base_class="NamespacedResource"),
        ]

        with patch("class_generator.core.discovery.ResourceScanner", return_value=mock_scanner):
            # Discover resources
            resources = discover_generated_resources()

        # Verify only pod.py is found
        assert len(resources) == 1
        assert resources[0]["kind"] == "Pod"

    def test_discover_handles_multiple_classes(self, temp_resources_dir, monkeypatch):
        """Test discovery handles files with multiple classes correctly."""
        # Create a file with multiple classes
        content = '''# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from ocp_resources.resource import NamespacedResource, Resource


class Helper:
    """Helper class."""
    pass


class MainResource(NamespacedResource):
    """Main resource class."""
    pass


class AnotherResource(Resource):
    """Another resource class."""
    pass
'''
        test_file = temp_resources_dir / "multi_class.py"
        test_file.write_text(content)

        # Mock ResourceScanner - it finds the first resource class
        mock_scanner = MagicMock()
        mock_scanner.scan_resources.return_value = [
            ResourceInfo(name="MainResource", file_path=str(test_file), base_class="NamespacedResource"),
        ]

        with patch("class_generator.core.discovery.ResourceScanner", return_value=mock_scanner):
            # Discover resources
            resources = discover_generated_resources()

        # Verify it finds the first resource class
        assert len(resources) == 1
        assert resources[0]["kind"] == "MainResource"

    def test_discover_empty_directory(self, temp_resources_dir, monkeypatch):
        """Test discovery handles empty directory gracefully."""
        # Mock ResourceScanner with empty result
        mock_scanner = MagicMock()
        mock_scanner.scan_resources.return_value = []

        with patch("class_generator.core.discovery.ResourceScanner", return_value=mock_scanner):
            # Discover resources
            resources = discover_generated_resources()

        # Verify empty list is returned
        assert resources == []

    def test_discover_detects_user_code(self, temp_resources_dir, monkeypatch):
        """Test discovery correctly detects presence of user code."""
        # Create files with and without user code
        file_with_user_code = temp_resources_dir / "custom_pod.py"
        self.create_generated_file(file_with_user_code, "CustomPod", with_user_code=True)

        file_without_user_code = temp_resources_dir / "basic_pod.py"
        self.create_generated_file(file_without_user_code, "BasicPod", with_user_code=False)

        # Mock ResourceScanner
        mock_scanner = MagicMock()
        mock_scanner.scan_resources.return_value = [
            ResourceInfo(name="BasicPod", file_path=str(file_without_user_code), base_class="NamespacedResource"),
            ResourceInfo(name="CustomPod", file_path=str(file_with_user_code), base_class="NamespacedResource"),
        ]

        with patch("class_generator.core.discovery.ResourceScanner", return_value=mock_scanner):
            # Discover resources
            resources = discover_generated_resources()

        # Sort by kind for consistent testing
        resources.sort(key=lambda r: r["kind"])

        # Verify user code detection
        assert resources[0]["kind"] == "BasicPod"
        assert resources[0]["has_user_code"] is False

        assert resources[1]["kind"] == "CustomPod"
        assert resources[1]["has_user_code"] is True
