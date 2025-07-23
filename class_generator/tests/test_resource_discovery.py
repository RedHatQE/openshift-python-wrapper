"""Tests for resource discovery functionality in class_generator."""

import json
import tempfile
import time
from typing import Any
from unittest.mock import MagicMock, patch, mock_open

import pytest

from class_generator.class_generator import discover_cluster_resources, analyze_coverage, generate_report
from fake_kubernetes_client.dynamic_client import FakeDynamicClient


class TestResourceDiscovery:
    """Test cases for discover_cluster_resources function."""

    @pytest.fixture
    def fake_client(self) -> FakeDynamicClient:
        """Create a fake dynamic client for testing."""
        return FakeDynamicClient()

    @pytest.fixture
    def sample_api_resources(self) -> dict[str, list[dict[str, Any]]]:
        """Sample API resources for testing."""
        return {
            "v1": [
                {"name": "pods", "kind": "Pod", "namespaced": True},
                {"name": "services", "kind": "Service", "namespaced": True},
                {"name": "configmaps", "kind": "ConfigMap", "namespaced": True},
                {"name": "nodes", "kind": "Node", "namespaced": False},
            ],
            "apps/v1": [
                {"name": "deployments", "kind": "Deployment", "namespaced": True},
                {"name": "replicasets", "kind": "ReplicaSet", "namespaced": True},
                {"name": "daemonsets", "kind": "DaemonSet", "namespaced": True},
            ],
            "route.openshift.io/v1": [
                {"name": "routes", "kind": "Route", "namespaced": True},
            ],
            "custom.io/v1": [
                {"name": "customresources", "kind": "CustomResource", "namespaced": True},
            ],
        }

    @pytest.fixture
    def sample_discovered_resources(self) -> dict[str, list[dict[str, Any]]]:
        """Sample discovered resources for coverage testing."""
        return {
            "v1": [
                {"name": "pods", "kind": "Pod", "namespaced": True},
                {"name": "services", "kind": "Service", "namespaced": True},
                {"name": "configmaps", "kind": "ConfigMap", "namespaced": True},
                {"name": "secrets", "kind": "Secret", "namespaced": True},
            ],
            "apps/v1": [
                {"name": "deployments", "kind": "Deployment", "namespaced": True},
                {"name": "statefulsets", "kind": "StatefulSet", "namespaced": True},
            ],
            "route.openshift.io/v1": [
                {"name": "routes", "kind": "Route", "namespaced": True},
            ],
        }

    def test_discover_cluster_resources_success(
        self, fake_client: FakeDynamicClient, sample_api_resources: dict[str, list[dict[str, Any]]]
    ) -> None:
        """Test successful resource discovery using direct API calls."""
        # Mock the client's call_api method directly
        with patch.object(fake_client.client, "call_api") as mock_call_api:

            def mock_call_api_impl(resource_path=None, method=None, **kwargs):
                # Mock core API resources response
                if resource_path == "/api/v1" and method == "GET":
                    return {
                        "resources": [
                            {"name": r["name"], "kind": r["kind"], "namespaced": r["namespaced"]}
                            for r in sample_api_resources["v1"]
                        ]
                    }

                # Mock API groups response
                elif resource_path == "/apis" and method == "GET":
                    return {
                        "groups": [
                            {"name": "apps", "versions": [{"groupVersion": "apps/v1"}]},
                            {"name": "route.openshift.io", "versions": [{"groupVersion": "route.openshift.io/v1"}]},
                        ]
                    }

                # Mock specific API group resources
                elif resource_path == "/apis/apps/v1" and method == "GET":
                    return {
                        "resources": [
                            {"name": r["name"], "kind": r["kind"], "namespaced": r["namespaced"]}
                            for r in sample_api_resources.get("apps/v1", [])
                        ]
                    }

                elif resource_path == "/apis/route.openshift.io/v1" and method == "GET":
                    return {
                        "resources": [
                            {"name": r["name"], "kind": r["kind"], "namespaced": r["namespaced"]}
                            for r in sample_api_resources.get("route.openshift.io/v1", [])
                        ]
                    }

                return {"resources": []}

            mock_call_api.side_effect = mock_call_api_impl

            # Mock resources.get for CRD discovery
            with patch.object(fake_client.resources, "get") as mock_get:
                # CRD discovery should raise exception (no CRDs)
                mock_get.side_effect = Exception("No CRDs")

                discovered = discover_cluster_resources(client=fake_client)

            # Verify structure
            assert isinstance(discovered, dict)
            assert all(isinstance(v, list) for v in discovered.values())

            # Verify we have some resources discovered
            assert "v1" in discovered
            assert len(discovered["v1"]) > 0

            # Check that discovered resources have the right structure
            for resources in discovered.values():
                for r in resources:
                    assert "name" in r
                    assert "kind" in r
                    assert "namespaced" in r

    def test_discover_cluster_resources_with_crds(self, fake_client: FakeDynamicClient) -> None:
        """Test discovery including CRDs."""
        with patch.object(fake_client.resources, "get") as mock_get:

            def mock_get_side_effect(api_version=None, kind=None, **kwargs):
                mock_resource = MagicMock()

                # Handle APIGroup request
                if kind == "APIGroup":
                    raise Exception("APIGroup not found")

                # Handle testing for common groups
                if kind is None:
                    raise Exception("Group not found")

                # Handle APIResourceList for core API
                if kind == "APIResourceList" and api_version == "v1":
                    mock_pod = MagicMock()
                    mock_pod.name = "pods"
                    mock_pod.kind = "Pod"
                    mock_pod.namespaced = True

                    mock_response = MagicMock()
                    mock_response.resources = [mock_pod]
                    mock_resource.get.return_value = mock_response

                # Handle CRD requests
                if kind == "CustomResourceDefinition":
                    # Create mock CRD
                    mock_crd = MagicMock()
                    mock_crd.spec.group = "custom.io"
                    mock_crd.spec.scope = "Namespaced"
                    mock_crd.spec.names.kind = "CustomResource"
                    mock_crd.spec.names.plural = "customresources"

                    mock_version = MagicMock()
                    mock_version.name = "v1"
                    mock_version.served = True
                    mock_crd.spec.versions = [mock_version]

                    mock_response = MagicMock()
                    mock_response.items = [mock_crd]
                    mock_resource.get.return_value = mock_response

                return mock_resource

            mock_get.side_effect = mock_get_side_effect

            discovered = discover_cluster_resources(client=fake_client)

            # Should have CRD resources
            assert "custom.io/v1" in discovered
            assert any(r["kind"] == "CustomResource" for r in discovered.get("custom.io/v1", []))

    def test_discover_cluster_resources_with_filter(self, fake_client: FakeDynamicClient) -> None:
        """Test resource discovery with API group filter."""
        with patch.object(fake_client.resources, "get") as mock_get:

            def mock_get_side_effect(api_version=None, kind=None, **kwargs):
                mock_resource = MagicMock()

                # Handle APIGroup request
                if kind == "APIGroup":
                    raise Exception("APIGroup not found")

                # Handle testing for common groups
                if kind is None and "apps" in api_version:
                    return mock_resource  # apps group exists
                elif kind is None:
                    raise Exception("Group not found")

                # Handle APIResourceList
                if kind == "APIResourceList":
                    if api_version == "apps/v1":
                        mock_deployment = MagicMock()
                        mock_deployment.name = "deployments"
                        mock_deployment.kind = "Deployment"
                        mock_deployment.namespaced = True

                        mock_response = MagicMock()
                        mock_response.resources = [mock_deployment]
                        mock_resource.get.return_value = mock_response
                    else:
                        mock_response = MagicMock()
                        mock_response.resources = []
                        mock_resource.get.return_value = mock_response

                # No CRDs
                if kind == "CustomResourceDefinition":
                    raise Exception("No CRDs")

                return mock_resource

            mock_get.side_effect = mock_get_side_effect

            # Filter for only apps group
            discovered = discover_cluster_resources(client=fake_client, api_group_filter="apps")

            # Should only have apps/* API groups
            assert all(k.startswith("apps/") for k in discovered.keys())
            assert "v1" not in discovered  # Core API group should be filtered out

    def test_discover_cluster_resources_connection_error(self, fake_client: FakeDynamicClient) -> None:
        """Test handling of connection errors."""
        # The implementation currently catches exceptions and returns an empty dict
        with patch.object(fake_client.resources, "get", side_effect=Exception("Connection refused")):
            discovered = discover_cluster_resources(client=fake_client)

            # Should return empty dict on connection error
            assert discovered == {}

    def test_discover_cluster_resources_empty_cluster(self, fake_client: FakeDynamicClient) -> None:
        """Test discovery on cluster with no resources."""
        with patch.object(fake_client.resources, "get") as mock_get:

            def mock_get_side_effect(api_version=None, kind=None, **kwargs):
                mock_resource = MagicMock()

                # Handle APIGroup request
                if kind == "APIGroup":
                    raise Exception("APIGroup not found")

                # All groups don't exist
                if kind is None:
                    raise Exception("Group not found")

                # Handle APIResourceList for core API (empty)
                if kind == "APIResourceList" and api_version == "v1":
                    mock_response = MagicMock()
                    mock_response.resources = []
                    mock_resource.get.return_value = mock_response

                # No CRDs
                if kind == "CustomResourceDefinition":
                    raise Exception("No CRDs")

                return mock_resource

            mock_get.side_effect = mock_get_side_effect

            discovered = discover_cluster_resources(client=fake_client)

            # Should return empty dict or dict with empty lists
            assert isinstance(discovered, dict)
            assert all(len(resources) == 0 for resources in discovered.values())


class TestCoverageAnalysis:
    """Test cases for analyze_coverage function."""

    @pytest.fixture
    def sample_discovered_resources(self) -> dict[str, list[dict[str, Any]]]:
        """Sample discovered resources for coverage testing."""
        return {
            "v1": [
                {"name": "pods", "kind": "Pod", "namespaced": True},
                {"name": "services", "kind": "Service", "namespaced": True},
                {"name": "configmaps", "kind": "ConfigMap", "namespaced": True},
                {"name": "secrets", "kind": "Secret", "namespaced": True},
                {"name": "nodes", "kind": "Node", "namespaced": False},
            ],
            "apps/v1": [
                {"name": "deployments", "kind": "Deployment", "namespaced": True},
                {"name": "statefulsets", "kind": "StatefulSet", "namespaced": True},
                {"name": "replicasets", "kind": "ReplicaSet", "namespaced": True},
            ],
            "route.openshift.io/v1": [
                {"name": "routes", "kind": "Route", "namespaced": True},
            ],
            "networking.k8s.io/v1": [
                {"name": "networkpolicies", "kind": "NetworkPolicy", "namespaced": True},
            ],
        }

    @pytest.fixture
    def mock_ocp_resources_files(self) -> list[str]:
        """Mock list of files in ocp_resources directory."""
        return [
            "__init__.py",
            "pod.py",
            "service.py",
            "deployment.py",
            "config_map.py",  # Note: filename uses snake_case
            "route.py",
            "dns_config_openshift_io.py",  # Special case: DNS has multiple files
            "dns_operator_openshift_io.py",  # Special case: DNS has multiple files
            "utils/constants.py",  # Should be ignored
            "README.md",  # Should be ignored
        ]

    def test_analyze_coverage_basic(
        self, sample_discovered_resources: dict[str, list[dict[str, Any]]], mock_ocp_resources_files: list[str]
    ) -> None:
        """Test basic coverage analysis."""
        with patch("os.listdir", return_value=mock_ocp_resources_files):
            with patch("os.path.isfile", return_value=True):
                with patch("os.path.exists", return_value=True):
                    # Mock reading the files to determine what resource they implement
                    def mock_file_open(filepath, mode="r"):
                        content = ""
                        if "pod.py" in filepath:
                            content = 'class Pod(NamespacedResource):\n    """Pod resource"""'
                        elif "service.py" in filepath:
                            content = 'class Service(NamespacedResource):\n    """Service resource"""'
                        elif "deployment.py" in filepath:
                            content = 'class Deployment(NamespacedResource):\n    """Deployment resource"""'
                        elif "config_map.py" in filepath:
                            content = 'class ConfigMap(NamespacedResource):\n    """ConfigMap resource"""'
                        elif "route.py" in filepath:
                            content = 'class Route(NamespacedResource):\n    """Route resource"""'
                        elif "dns_config" in filepath:
                            content = 'class DNS(NamespacedResource):\n    """DNS config resource"""'
                        elif "dns_operator" in filepath:
                            content = 'class DNS(NamespacedResource):\n    """DNS operator resource"""'
                        return mock_open(read_data=content)()

                    with patch("builtins.open", side_effect=mock_file_open):
                        analysis = analyze_coverage(discovered_resources=sample_discovered_resources)

                # Verify structure
                assert "implemented_resources" in analysis
                assert "missing_resources" in analysis
                assert "coverage_stats" in analysis

                # Check implemented resources
                assert "Pod" in analysis["implemented_resources"]
                assert "Service" in analysis["implemented_resources"]
                assert "Deployment" in analysis["implemented_resources"]
                assert "ConfigMap" in analysis["implemented_resources"]
                assert "Route" in analysis["implemented_resources"]

                # Check missing resources
                assert any(r["kind"] == "Secret" for r in analysis["missing_resources"])
                assert any(r["kind"] == "Node" for r in analysis["missing_resources"])
                assert any(r["kind"] == "StatefulSet" for r in analysis["missing_resources"])
                assert any(r["kind"] == "NetworkPolicy" for r in analysis["missing_resources"])

                # Check coverage stats
                stats = analysis["coverage_stats"]
                assert stats["total_discovered"] == 10  # Total resources in discovered_resources
                assert stats["total_implemented"] == 6  # All implemented including DNS
                assert stats["covered_resources"] == 5  # Only Pod, Service, Deployment, ConfigMap, Route (not DNS)
                assert stats["total_missing"] == 5  # Secret, Node, StatefulSet, ReplicaSet, NetworkPolicy
                assert stats["coverage_percentage"] == 50.0  # 5 covered out of 10 discovered

    def test_analyze_coverage_with_special_cases(
        self, sample_discovered_resources: dict[str, list[dict[str, Any]]]
    ) -> None:
        """Test coverage analysis with special cases like DNS having multiple files."""
        files_with_dns = [
            "dns_config_openshift_io.py",
            "dns_operator_openshift_io.py",
            "network_operator_openshift_io.py",
        ]

        with patch("os.listdir", return_value=files_with_dns):
            with patch("os.path.isfile", return_value=True):
                with patch("os.path.exists", return_value=True):

                    def mock_file_open(filepath, mode="r"):
                        # All DNS files implement the DNS resource
                        content = ""
                        if "dns_" in filepath:
                            content = 'class DNS(Resource):\n    """DNS resource"""'
                        elif "network_operator" in filepath:
                            content = 'class Network(Resource):\n    """Network resource"""'
                        return mock_open(read_data=content)()

                    with patch("builtins.open", side_effect=mock_file_open):
                        # Add DNS to discovered resources
                        discovered_with_dns = sample_discovered_resources.copy()
                        discovered_with_dns["config.openshift.io/v1"] = [
                            {"name": "dnses", "kind": "DNS", "namespaced": False}
                        ]

                        analysis = analyze_coverage(discovered_resources=discovered_with_dns)

                # DNS should be counted only once despite multiple files
                assert "DNS" in analysis["implemented_resources"]
                dns_count = sum(1 for r in analysis["implemented_resources"] if r == "DNS")
                assert dns_count == 1

    def test_analyze_coverage_empty_directory(
        self, sample_discovered_resources: dict[str, list[dict[str, Any]]]
    ) -> None:
        """Test coverage analysis with empty ocp_resources directory."""
        with patch("os.listdir", return_value=[]):
            with patch("os.path.exists", return_value=True):
                analysis = analyze_coverage(discovered_resources=sample_discovered_resources)

            assert analysis["implemented_resources"] == []
            assert len(analysis["missing_resources"]) == 10  # All discovered resources are missing
            assert analysis["coverage_stats"]["coverage_percentage"] == 0.0

    def test_analyze_coverage_no_discovered_resources(self) -> None:
        """Test coverage analysis with no discovered resources."""
        with patch("os.listdir", return_value=["pod.py", "service.py"]):
            with patch("os.path.exists", return_value=True):
                analysis = analyze_coverage(discovered_resources={})

            assert analysis["coverage_stats"]["total_discovered"] == 0
            assert analysis["coverage_stats"]["coverage_percentage"] == 0.0  # No resources to cover

    def test_analyze_coverage_filters_non_python_files(
        self, sample_discovered_resources: dict[str, list[dict[str, Any]]]
    ) -> None:
        """Test that non-Python files and utility files are filtered out."""
        mixed_files = [
            "pod.py",
            "README.md",
            "__init__.py",
            "utils.py",
            "constants.py",
            "__pycache__/",
            "test_pod.py",
            "service.py",
        ]

        with patch("os.listdir", return_value=mixed_files):
            with patch("os.path.isfile") as mock_isfile:
                with patch("os.path.exists", return_value=True):
                    # Only .py files that aren't __init__.py or in utils
                    mock_isfile.side_effect = lambda x: x.endswith(".py") and not x.endswith("__pycache__/")

                    def mock_file_open(filepath, mode="r"):
                        content = ""
                        if "pod.py" in filepath:
                            content = 'class Pod(NamespacedResource):\n    """Pod resource"""'
                        elif "service.py" in filepath:
                            content = 'class Service(NamespacedResource):\n    """Service resource"""'
                        return mock_open(read_data=content)()

                    with patch("builtins.open", side_effect=mock_file_open):
                        analysis = analyze_coverage(discovered_resources=sample_discovered_resources)

                # Only Pod and Service should be detected
                assert len(analysis["implemented_resources"]) == 2
                assert "Pod" in analysis["implemented_resources"]
                assert "Service" in analysis["implemented_resources"]


class TestReportGeneration:
    """Test cases for generate_report function."""

    @pytest.fixture
    def sample_coverage_analysis(self) -> dict[str, Any]:
        """Sample coverage analysis result."""
        return {
            "implemented_resources": ["Pod", "Service", "Deployment", "ConfigMap", "Route"],
            "missing_resources": [
                {"kind": "Secret", "api_version": "v1", "name": "secrets", "namespaced": True},
                {"kind": "Node", "api_version": "v1", "name": "nodes", "namespaced": False},
                {"kind": "StatefulSet", "api_version": "apps/v1", "name": "statefulsets", "namespaced": True},
                {
                    "kind": "NetworkPolicy",
                    "api_version": "networking.k8s.io/v1",
                    "name": "networkpolicies",
                    "namespaced": True,
                },
                {
                    "kind": "VirtualMachine",
                    "api_version": "kubevirt.io/v1",
                    "name": "virtualmachines",
                    "namespaced": True,
                },
            ],
            "coverage_stats": {
                "total_discovered": 10,
                "total_implemented": 5,
                "covered_resources": 5,
                "total_missing": 5,
                "coverage_percentage": 50.0,
            },
        }

    def test_generate_report_human_readable(self, sample_coverage_analysis: dict[str, Any]) -> None:
        """Test human-readable report generation."""
        report = generate_report(coverage_analysis=sample_coverage_analysis, output_format="human")

        # Check that report contains key sections
        assert "Coverage Report" in report
        assert "Coverage Statistics" in report
        assert "50.0%" in report  # Coverage percentage
        assert "Missing Resources" in report

        # Check that missing resources are listed
        assert "Secret" in report
        assert "Node" in report
        assert "StatefulSet" in report
        assert "NetworkPolicy" in report

        # Check priority indicators (core resources should be marked)
        assert "CORE" in report or "HIGH" in report  # Secret and Node are core v1 resources

    def test_generate_report_json(self, sample_coverage_analysis: dict[str, Any]) -> None:
        """Test JSON report generation."""
        report = generate_report(coverage_analysis=sample_coverage_analysis, output_format="json")

        # Parse JSON
        report_data = json.loads(report)

        # Check structure
        assert "coverage_stats" in report_data
        assert "missing_resources" in report_data
        assert "implemented_resources" in report_data
        assert "generation_commands" in report_data

        # Check stats
        assert report_data["coverage_stats"]["coverage_percentage"] == 50.0

        # Check generation commands
        commands = report_data["generation_commands"]
        assert len(commands) > 0
        # Should have commands for missing resources
        assert any("Secret" in cmd for cmd in commands)

    def test_generate_report_with_priority_scoring(self, sample_coverage_analysis: dict[str, Any]) -> None:
        """Test that resources are prioritized correctly."""
        report = generate_report(coverage_analysis=sample_coverage_analysis, output_format="json")

        report_data = json.loads(report)
        missing_resources = report_data["missing_resources"]

        # Core resources (v1) should have higher priority
        secret = next(r for r in missing_resources if r["kind"] == "Secret")
        vm = next(r for r in missing_resources if r["kind"] == "VirtualMachine")

        assert secret.get("priority", 0) > vm.get("priority", 0)

    def test_generate_report_class_generator_commands(self, sample_coverage_analysis: dict[str, Any]) -> None:
        """Test generation of ready-to-use class-generator commands."""
        report = generate_report(coverage_analysis=sample_coverage_analysis, output_format="json")

        report_data = json.loads(report)
        commands = report_data["generation_commands"]

        # Check command structure
        for cmd in commands:
            assert "class-generator" in cmd
            assert "-k" in cmd or "--kind" in cmd
            # Should not have -g or -v flags (they don't exist)
            assert " -g " not in cmd
            assert " -v " not in cmd

        # Check batch command generation
        batch_commands = report_data.get("batch_generation_commands", [])
        if batch_commands:
            # Should group by API version
            assert any("Secret,Node" in cmd for cmd in batch_commands)  # Both are v1
            # Batch commands should also not have -g or -v flags
            for cmd in batch_commands:
                assert " -g " not in cmd
                assert " -v " not in cmd

    def test_generate_report_empty_missing_resources(self) -> None:
        """Test report generation when all resources are implemented."""
        coverage_analysis = {
            "implemented_resources": ["Pod", "Service"],
            "missing_resources": [],
            "coverage_stats": {
                "total_discovered": 2,
                "total_implemented": 2,
                "covered_resources": 2,
                "total_missing": 0,
                "coverage_percentage": 100.0,
            },
        }

        report = generate_report(coverage_analysis=coverage_analysis, output_format="human")

        assert "100.0%" in report
        assert "All resources are implemented" in report or "No missing resources" in report


class TestCLIIntegration:
    """Test cases for CLI integration of resource discovery features."""

    def test_discover_missing_flag(self) -> None:
        """Test --discover-missing flag functionality."""
        from click.testing import CliRunner
        from class_generator.class_generator import main

        runner = CliRunner()

        with tempfile.TemporaryDirectory() as tmpdir:
            # Mock expanduser to use temp directory (avoid real cache)
            with patch("os.path.expanduser") as mock_expanduser:
                mock_expanduser.return_value = tmpdir

                # Mock the discovery and analysis functions
                with patch("class_generator.class_generator.discover_cluster_resources") as mock_discover:
                    with patch("class_generator.class_generator.analyze_coverage") as mock_analyze:
                        with patch("class_generator.class_generator.generate_report") as mock_report:
                            # Set up mock returns
                            mock_discover.return_value = {"v1": [{"name": "pods", "kind": "Pod", "namespaced": True}]}
                            mock_analyze.return_value = {
                                "missing_resources": [],
                                "coverage_stats": {"coverage_percentage": 100.0},
                            }
                            mock_report.return_value = "Coverage Report"

                            # Run CLI with discover-missing flag
                            result = runner.invoke(cli=main, args=["--discover-missing"])

                            # Check that functions were called
                            assert mock_discover.called
                            assert mock_analyze.called
                            assert mock_report.called

                            # Check output
                            assert result.exit_code == 0
                            assert "Coverage Report" in result.output

    def test_coverage_report_with_json_flag(self) -> None:
        """Test --coverage-report with --json flag."""
        from click.testing import CliRunner
        from class_generator.class_generator import main

        runner = CliRunner()

        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("os.path.expanduser") as mock_expanduser:
                mock_expanduser.return_value = tmpdir

                with patch("class_generator.class_generator.discover_cluster_resources") as mock_discover:
                    with patch("class_generator.class_generator.analyze_coverage") as mock_analyze:
                        with patch("class_generator.class_generator.generate_report") as mock_report:
                            mock_discover.return_value = {"v1": []}
                            mock_analyze.return_value = {"missing_resources": []}
                            # Return JSON format
                            mock_report.return_value = json.dumps(
                                {"coverage_stats": {"coverage_percentage": 100.0}}, indent=2
                            )

                            # Test JSON format
                            result = runner.invoke(cli=main, args=["--coverage-report", "--json"])

                            assert result.exit_code == 0
                            mock_report.assert_called_with(
                                coverage_analysis=mock_analyze.return_value, output_format="json"
                            )

    def test_discover_missing_with_caching(self) -> None:
        """Test that discovery results are cached."""
        from click.testing import CliRunner
        from class_generator.class_generator import main
        import os

        runner = CliRunner()

        with tempfile.TemporaryDirectory() as tmpdir:
            # Mock expanduser to return a path inside tmpdir
            home_dir = os.path.join(tmpdir, "home")
            os.makedirs(home_dir)

            cache_dir = os.path.join(home_dir, ".cache", "openshift-python-wrapper")
            cache_file = os.path.join(cache_dir, "discovery_cache.json")

            # Ensure cache directory exists
            os.makedirs(cache_dir, exist_ok=True)

            # Write initial cache file to test caching behavior
            with open(cache_file, "w") as f:
                json.dump(
                    {"discovered_resources": {"v1": [{"name": "pods", "kind": "Pod"}]}, "timestamp": time.time()}, f
                )

            with patch("os.path.expanduser") as mock_expanduser:
                # Make expanduser return our test home directory
                def expanduser_side_effect(path):
                    if path.startswith("~"):
                        return path.replace("~", home_dir, 1)
                    return path

                mock_expanduser.side_effect = expanduser_side_effect

                with patch("class_generator.class_generator.discover_cluster_resources") as mock_discover:
                    with patch("class_generator.class_generator.analyze_coverage") as mock_analyze:
                        with patch("class_generator.class_generator.generate_report") as mock_report:
                            mock_discover.return_value = {"v1": [{"name": "pods", "kind": "Pod"}]}
                            mock_analyze.return_value = {"missing_resources": [], "coverage_stats": {}}
                            mock_report.return_value = "Report"

                            # Run with cache - should not call discover
                            result = runner.invoke(cli=main, args=["--discover-missing"])

                            # Debug output
                            if result.exit_code != 0:
                                print(f"Exit code: {result.exit_code}")
                                print(f"Output: {result.output}")
                                print(f"Exception: {result.exception}")

                            assert result.exit_code == 0

                            # Check if cache was used
                            if "Using cached discovery results" not in result.output:
                                print(f"Output: {result.output}")
                                print(f"Cache file exists: {os.path.exists(cache_file)}")
                                print(f"Cache dir: {cache_dir}")
                                print(f"Expanduser called with: {mock_expanduser.call_args}")

                            # Should use cache, not call discover
                            assert mock_discover.call_count == 0
                            assert mock_analyze.called
                            assert mock_report.called

    def test_discover_missing_with_kind_generation(self) -> None:
        """Test that --discover-missing can be combined with kind generation."""
        from click.testing import CliRunner
        from class_generator.class_generator import main

        runner = CliRunner()

        with patch("class_generator.class_generator.discover_cluster_resources") as mock_discover:
            with patch("class_generator.class_generator.analyze_coverage") as mock_analyze:
                with patch("class_generator.class_generator.generate_report") as mock_report:
                    with patch("class_generator.class_generator.class_generator") as mock_generator:
                        mock_discover.return_value = {
                            "v1": [
                                {"name": "secrets", "kind": "Secret", "namespaced": True},
                                {"name": "pods", "kind": "Pod", "namespaced": True},
                            ]
                        }
                        mock_analyze.return_value = {
                            "missing_resources": [{"kind": "Secret", "api_version": "v1"}],
                            "coverage_stats": {"coverage_percentage": 50.0},
                        }
                        mock_report.return_value = "Report"

                        # Run with both discover and generate for missing resource
                        result = runner.invoke(cli=main, args=["--discover-missing", "--generate-missing"])

                        assert result.exit_code == 0
                        # Should generate class for missing Secret resource
                        mock_generator.assert_called()
                        assert any("Secret" in str(call) for call in mock_generator.call_args_list)
