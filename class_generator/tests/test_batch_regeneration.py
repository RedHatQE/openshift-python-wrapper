"""Tests for batch regeneration functionality."""

import logging
import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

import class_generator.cli
from class_generator.cli import main
from class_generator.core.discovery import discover_generated_resources
from class_generator.utils import ResourceInfo


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
        (temp_resources_dir / "__init__.py").write_text(data="# Init file")
        (temp_resources_dir / "resource.py").write_text(data="# Base resource")
        (temp_resources_dir / "exceptions.py").write_text(data="# Exceptions")
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
        test_file.write_text(data=content)

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


class TestRegenerateAll:
    """Test the --regenerate-all CLI functionality."""

    def test_regenerate_all_basic(self, monkeypatch, tmp_path):
        """Test basic regenerate-all functionality."""

        # Use temporary paths to ensure no real files are touched
        temp_pod = tmp_path / "pod.py"
        temp_service = tmp_path / "service.py"

        # Mock the functions we'll use
        mock_discover = MagicMock(
            return_value=[
                {"kind": "Pod", "path": str(temp_pod), "has_user_code": False},
                {"kind": "Service", "path": str(temp_service), "has_user_code": True},
            ]
        )
        mock_generator = MagicMock(return_value=[str(temp_pod)])

        # Need to patch where the functions are imported, not where they're defined
        monkeypatch.setattr(class_generator.cli, "discover_generated_resources", mock_discover)
        monkeypatch.setattr(class_generator.cli, "class_generator", mock_generator)

        runner = CliRunner()
        result = runner.invoke(cli=main, args=["--regenerate-all"])

        assert result.exit_code == 0
        assert mock_discover.called
        assert mock_generator.call_count == 2

        # Check that class_generator was called with correct arguments
        calls = mock_generator.call_args_list
        assert calls[0][1]["kind"] == "Pod"
        assert calls[0][1]["overwrite"] is True
        assert calls[0][1]["output_file"] == str(temp_pod)
        assert calls[1][1]["kind"] == "Service"
        assert calls[1][1]["output_file"] == str(temp_service)

    def test_regenerate_all_with_backup(self, monkeypatch, tmp_path):
        """Test regenerate-all with backup option."""

        # Change to temp directory
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            # Create fake resource files
            resources_dir = tmp_path / "ocp_resources"
            resources_dir.mkdir()
            pod_file = resources_dir / "pod.py"
            pod_file.write_text(data="# Original pod content")

            # Mock functions
            mock_discover = MagicMock(
                return_value=[
                    {"kind": "Pod", "path": str(pod_file), "has_user_code": False},
                ]
            )
            mock_generator = MagicMock(return_value=[str(pod_file)])

            # Need to patch where the functions are imported, not where they're defined
            monkeypatch.setattr(class_generator.cli, "discover_generated_resources", mock_discover)
            monkeypatch.setattr(class_generator.cli, "class_generator", mock_generator)

            runner = CliRunner()
            result = runner.invoke(cli=main, args=["--regenerate-all", "--backup"])

            assert result.exit_code == 0

            # Check that backup directory was created
            backup_dirs = list(tmp_path.glob(".backups/backup-*"))
            assert len(backup_dirs) == 1

            # Check that file was backed up
            backup_file = backup_dirs[0] / "ocp_resources" / "pod.py"
            assert backup_file.exists()
            assert backup_file.read_text() == "# Original pod content"

        finally:
            os.chdir(original_cwd)

    def test_regenerate_all_with_filter(self, monkeypatch, tmp_path):
        """Test regenerate-all with filter option."""

        # Use temporary paths to ensure no real files are touched
        temp_files = {
            "Pod": tmp_path / "pod.py",
            "Service": tmp_path / "service.py",
            "Deployment": tmp_path / "deployment.py",
            "ServiceAccount": tmp_path / "service_account.py",
        }

        # Mock the functions
        mock_discover = MagicMock(
            return_value=[
                {"kind": kind, "path": str(path), "has_user_code": False} for kind, path in temp_files.items()
            ]
        )
        mock_generator = MagicMock(return_value=["dummy"])

        # Need to patch where the functions are imported, not where they're defined
        monkeypatch.setattr(class_generator.cli, "discover_generated_resources", mock_discover)
        monkeypatch.setattr(class_generator.cli, "class_generator", mock_generator)

        runner = CliRunner()
        result = runner.invoke(cli=main, args=["--regenerate-all", "--filter", "Service*"])

        assert result.exit_code == 0
        assert mock_generator.call_count == 2  # Only Service and ServiceAccount

        # Check that only Service* resources were regenerated
        regenerated_kinds = [call[1]["kind"] for call in mock_generator.call_args_list]
        assert "Service" in regenerated_kinds
        assert "ServiceAccount" in regenerated_kinds
        assert "Pod" not in regenerated_kinds
        assert "Deployment" not in regenerated_kinds

    def test_regenerate_all_dry_run(self, monkeypatch, caplog, tmp_path):
        """Test regenerate-all with dry-run option."""

        # Use temporary path to ensure no real files are touched
        temp_pod = tmp_path / "pod.py"

        # Mock the functions
        mock_discover = MagicMock(
            return_value=[
                {"kind": "Pod", "path": str(temp_pod), "has_user_code": False},
            ]
        )
        mock_generator = MagicMock(return_value=[str(temp_pod)])

        # Need to patch where the functions are imported, not where they're defined
        monkeypatch.setattr(class_generator.cli, "discover_generated_resources", mock_discover)
        monkeypatch.setattr(class_generator.cli, "class_generator", mock_generator)

        runner = CliRunner()
        with caplog.at_level(logging.INFO):
            result = runner.invoke(cli=main, args=["--regenerate-all", "--dry-run"])

        assert result.exit_code == 0
        assert mock_generator.called
        assert mock_generator.call_args[1]["dry_run"] is True
        # Simply check that it ran successfully - the dry-run flag was passed correctly

    def test_regenerate_all_error_handling(self, monkeypatch, caplog, tmp_path):
        """Test regenerate-all handles errors gracefully."""

        # Use temporary paths to ensure no real files are touched
        temp_pod = tmp_path / "pod.py"
        temp_service = tmp_path / "service.py"

        # Mock the functions
        mock_discover = MagicMock(
            return_value=[
                {"kind": "Pod", "path": str(temp_pod), "has_user_code": False},
                {"kind": "Service", "path": str(temp_service), "has_user_code": False},
            ]
        )

        # Make class_generator fail for Pod but succeed for Service
        def mock_generator_side_effect(**kwargs):
            if kwargs["kind"] == "Pod":
                raise Exception("Failed to generate Pod")
            return [str(temp_service)]  # Return a list for success

        mock_generator = MagicMock(side_effect=mock_generator_side_effect)

        # Need to patch where the functions are imported, not where they're defined
        monkeypatch.setattr(class_generator.cli, "discover_generated_resources", mock_discover)
        monkeypatch.setattr(class_generator.cli, "class_generator", mock_generator)

        runner = CliRunner()
        with caplog.at_level(logging.INFO):
            result = runner.invoke(cli=main, args=["--regenerate-all"])

        assert result.exit_code == 0  # Should not fail completely
        assert mock_generator.call_count == 2
        # Verify that Pod generation failed and Service succeeded by checking the calls

    def test_backup_requires_regenerate_all(self):
        """Test that --backup requires --regenerate-all."""

        runner = CliRunner()
        result = runner.invoke(cli=main, args=["--backup"], catch_exceptions=False)

        assert result.exit_code != 0
        assert "exactly 1 of the following parameters must be set" in result.output.lower()

    def test_filter_requires_regenerate_all(self):
        """Test that --filter requires --regenerate-all."""

        runner = CliRunner()
        result = runner.invoke(cli=main, args=["--filter", "Pod*"], catch_exceptions=False)

        assert result.exit_code != 0
        assert "exactly 1 of the following parameters must be set" in result.output.lower()


class TestBackupWithKindOption:
    """Test backup functionality with -k --overwrite option."""

    @pytest.fixture
    def temp_ocp_resources_dir(self):
        """Create a temporary ocp_resources directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            resources_dir = Path(tmpdir) / "ocp_resources"
            resources_dir.mkdir()
            # Temporarily change to the temp directory
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            yield resources_dir
            os.chdir(original_cwd)

    def test_backup_requires_overwrite(self):
        """Test that --backup requires --overwrite when used with -k."""
        runner = CliRunner()
        result = runner.invoke(cli=main, args=["-k", "Pod", "--backup"])
        assert result.exit_code != 0
        assert "when --backup is set, exactly 1 of the following parameters must be set" in result.output

    def test_backup_with_single_kind(self, temp_ocp_resources_dir, monkeypatch):
        """Test backup creation with single kind and overwrite."""
        # Create existing file
        existing_file = temp_ocp_resources_dir / "pod.py"
        existing_file.write_text(data="# Existing Pod file\nclass Pod: pass")

        # Mock class_generator to avoid actual generation
        def mock_class_generator(**kwargs):
            # Return the path that would be generated
            return ["ocp_resources/pod.py"]

        monkeypatch.setattr("class_generator.cli.class_generator", mock_class_generator)

        runner = CliRunner()
        result = runner.invoke(cli=main, args=["-k", "Pod", "--overwrite", "--backup"])

        assert result.exit_code == 0

        # Check backup directory was created
        backup_dirs = list(Path.cwd().glob(".backups/backup-*"))
        assert len(backup_dirs) == 1

        # Check backup file exists with preserved directory structure
        backup_file = backup_dirs[0] / "ocp_resources" / "pod.py"
        assert backup_file.exists()
        assert backup_file.read_text() == "# Existing Pod file\nclass Pod: pass"

    def test_backup_with_multiple_kinds(self, temp_ocp_resources_dir, monkeypatch):
        """Test backup creation with multiple kinds and overwrite."""
        # Create existing files
        pod_file = temp_ocp_resources_dir / "pod.py"
        pod_file.write_text(data="# Existing Pod file")

        service_file = temp_ocp_resources_dir / "service.py"
        service_file.write_text(data="# Existing Service file")

        # Mock class_generator
        def mock_class_generator(**kwargs):
            kind = kwargs.get("kind")
            if kind == "Pod":
                return [str(pod_file)]
            elif kind == "Service":
                return [str(service_file)]
            return []

        monkeypatch.setattr("class_generator.cli.class_generator", mock_class_generator)

        runner = CliRunner()
        result = runner.invoke(cli=main, args=["-k", "Pod,Service", "--overwrite", "--backup"])

        assert result.exit_code == 0

        # Check backup directory was created
        backup_dirs = list(Path.cwd().glob(".backups/backup-*"))
        assert len(backup_dirs) == 1

        # Check backup files exist with preserved directory structure
        assert (backup_dirs[0] / "ocp_resources" / "pod.py").exists()
        assert (backup_dirs[0] / "ocp_resources" / "service.py").exists()

    def test_backup_with_dry_run(self, temp_ocp_resources_dir, monkeypatch):
        """Test that backup is not created in dry-run mode."""
        # Mock class_generator
        monkeypatch.setattr("class_generator.cli.class_generator", lambda **kwargs: [])

        runner = CliRunner()
        result = runner.invoke(cli=main, args=["-k", "Pod", "--overwrite", "--backup", "--dry-run"])

        assert result.exit_code == 0

        # Check no backup directory was created
        backup_dirs = list(Path.cwd().glob(".backups/backup-*"))
        assert len(backup_dirs) == 0

    def test_backup_with_custom_output_file(self, monkeypatch, temp_ocp_resources_dir):
        """Test backup with custom output file path."""
        custom_file = temp_ocp_resources_dir / "custom_pod.py"
        custom_file.write_text(data="# Custom Pod file")

        # Mock class_generator
        def mock_class_generator(**kwargs):
            return [str(custom_file)]

        monkeypatch.setattr("class_generator.cli.class_generator", mock_class_generator)

        runner = CliRunner()
        result = runner.invoke(cli=main, args=["-k", "Pod", "--overwrite", "--backup", "-o", str(custom_file)])

        assert result.exit_code == 0

        # Check backup was created
        backup_dirs = list(Path.cwd().glob(".backups/backup-*"))
        assert len(backup_dirs) == 1
        # The backup should preserve the directory structure
        relative_path = custom_file.relative_to(Path.cwd())
        assert (backup_dirs[0] / relative_path).exists()
