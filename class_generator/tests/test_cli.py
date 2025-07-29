"""Tests for existing CLI functionality to ensure refactoring doesn't break anything."""

import json
from unittest.mock import patch

from click.testing import CliRunner

from class_generator.cli import main


class TestCLIFunctionality:
    """Test CLI commands and options."""

    def test_coverage_report_console_format(self):
        """Test --coverage-report with console output format."""
        runner = CliRunner()

        with patch("class_generator.cli.discover_cluster_resources") as mock_discover:
            with patch("class_generator.cli.analyze_coverage") as mock_analyze:
                with patch("class_generator.cli.generate_report") as mock_report:
                    # Mock discovery results
                    mock_discover.return_value = {"v1": ["Pod", "Service"]}

                    # Mock coverage analysis
                    mock_analyze.return_value = {
                        "missing_resources": [],
                        "extra_resources": [],
                        "coverage_stats": {
                            "total_discovered": 2,
                            "total_implemented": 2,
                            "coverage_percentage": 100.0,
                            "missing_count": 0,
                            "extra_count": 0,
                        },
                    }

                    # Console format returns None
                    mock_report.return_value = None

                    result = runner.invoke(main, ["--coverage-report"])

                    assert result.exit_code == 0
                    # Verify correct parameter names are used
                    mock_report.assert_called_with(
                        coverage_data=mock_analyze.return_value,  # Not coverage_analysis!
                        output_format=None,  # Not "console"!
                    )

    def test_coverage_report_json_format(self):
        """Test --coverage-report with JSON output format."""
        runner = CliRunner()

        with patch("class_generator.cli.discover_cluster_resources") as mock_discover:
            with patch("class_generator.cli.analyze_coverage") as mock_analyze:
                with patch("class_generator.cli.generate_report") as mock_report:
                    # Mock discovery results
                    mock_discover.return_value = {"v1": ["Pod", "Service"]}

                    # Mock coverage analysis
                    coverage_data = {
                        "missing_resources": [],
                        "extra_resources": [],
                        "coverage_stats": {"total_discovered": 2, "total_implemented": 2, "coverage_percentage": 100.0},
                    }
                    mock_analyze.return_value = coverage_data

                    # JSON format returns string
                    mock_report.return_value = json.dumps(coverage_data, indent=2)

                    result = runner.invoke(main, ["--coverage-report", "--json"])

                    assert result.exit_code == 0
                    mock_report.assert_called_with(coverage_data=mock_analyze.return_value, output_format="json")
                    # JSON output should be printed
                    assert json.loads(result.output)

    def test_discover_missing(self):
        """Test --discover-missing functionality."""
        runner = CliRunner()

        with patch("class_generator.cli.discover_cluster_resources") as mock_discover:
            with patch("class_generator.cli.analyze_coverage") as mock_analyze:
                with patch("class_generator.cli.generate_report") as mock_report:
                    mock_discover.return_value = {"v1": ["Pod", "Service", "ConfigMap"]}
                    mock_analyze.return_value = {
                        "missing_resources": ["ConfigMap"],
                        "extra_resources": [],
                        "coverage_stats": {"coverage_percentage": 66.7},
                    }
                    mock_report.return_value = None

                    result = runner.invoke(main, ["--discover-missing"])

                    assert result.exit_code == 0
                    # Discover should not be called anymore since we use schema
                    assert not mock_discover.called
                    assert mock_analyze.called
                    assert mock_report.called

    def test_update_schema(self):
        """Test --update-schema functionality."""
        runner = CliRunner()

        with patch("class_generator.cli.update_kind_schema") as mock_update:
            mock_update.return_value = True

            result = runner.invoke(main, ["--update-schema"])

            assert result.exit_code == 0
            assert mock_update.called

    def test_kind_generation(self):
        """Test generating a specific kind."""
        runner = CliRunner()

        with patch("class_generator.cli.class_generator") as mock_generator:
            mock_generator.return_value = None

            result = runner.invoke(main, ["-k", "Pod"])

            assert result.exit_code == 0
            mock_generator.assert_called_once()
            # Check that the kind parameter is passed
            call_args = mock_generator.call_args[1]
            assert call_args["kind"] == "Pod"

    def test_kind_generation_with_output_file(self):
        """Test generating a specific kind with output file."""
        runner = CliRunner()

        with patch("class_generator.cli.class_generator") as mock_generator:
            mock_generator.return_value = None

            result = runner.invoke(main, ["-k", "Pod", "-o", "pod.py"])

            assert result.exit_code == 0
            mock_generator.assert_called_once()
            call_args = mock_generator.call_args[1]
            assert call_args["kind"] == "Pod"
            assert call_args["output_file"] == "pod.py"

    def test_dry_run(self):
        """Test --dry-run flag."""
        runner = CliRunner()

        with patch("class_generator.cli.class_generator") as mock_generator:
            mock_generator.return_value = None

            result = runner.invoke(main, ["-k", "Pod", "--dry-run"])

            assert result.exit_code == 0
            mock_generator.assert_called_once()
            call_args = mock_generator.call_args[1]
            assert call_args["dry_run"] is True

    def test_add_tests(self):
        """Test --add-tests functionality with -k option."""
        runner = CliRunner()

        # --add-tests requires -k option
        with patch("class_generator.cli.generate_class_generator_tests") as mock_test_gen:
            mock_test_gen.return_value = None

            result = runner.invoke(main, ["-k", "Pod", "--add-tests"])

            assert result.exit_code == 0
            mock_test_gen.assert_called_once()

    def test_add_tests_requires_kind(self):
        """Test that --add-tests cannot be used alone."""
        runner = CliRunner()

        result = runner.invoke(main, ["--add-tests"], catch_exceptions=False)

        # Should fail because it doesn't satisfy our validation
        assert result.exit_code != 0
        # Error is printed to stderr, not stdout

    def test_overwrite_flag(self):
        """Test --overwrite flag functionality."""
        runner = CliRunner()

        with patch("class_generator.cli.class_generator") as mock_generator:
            mock_generator.return_value = None

            result = runner.invoke(main, ["-k", "Pod", "--overwrite"])

            assert result.exit_code == 0
            mock_generator.assert_called_once()
            call_args = mock_generator.call_args[1]
            assert call_args["overwrite"] is True

    def test_generate_missing(self):
        """Test --generate-missing functionality."""
        runner = CliRunner()

        with patch("class_generator.cli.analyze_coverage") as mock_analyze:
            with patch("class_generator.cli.class_generator") as mock_generator:
                mock_analyze.return_value = {
                    "missing_resources": ["ConfigMap"],
                    "generated_resources": [],
                    "manual_resources": [],
                    "coverage_stats": {
                        "coverage_percentage": 66.7,
                        "total_in_mapping": 3,
                        "total_generated": 2,
                        "total_manual": 0,
                        "missing_count": 1,
                    },
                }
                mock_generator.return_value = None

                result = runner.invoke(main, ["--generate-missing"], catch_exceptions=False)

                assert result.exit_code == 0
                assert mock_analyze.called
                # Should try to generate ConfigMap
                mock_generator.assert_called_once_with(
                    kind="ConfigMap", output_file="", overwrite=False, add_tests=False, dry_run=False
                )

    def test_mutual_exclusivity_constraints(self):
        """Test mutual exclusivity constraints."""
        runner = CliRunner()

        # Cannot use --add-tests without -k
        result = runner.invoke(main, ["--add-tests"])
        assert result.exit_code != 0

    def test_required_options(self):
        """Test that at least one main option is required."""
        runner = CliRunner()

        # No options should fail
        result = runner.invoke(main, [], catch_exceptions=False)
        assert result.exit_code != 0
        # Error is printed to stderr, not stdout
