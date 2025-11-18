"""Tests for new schema.py functions focused on coverage improvement."""

import json
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from class_generator.constants import RESOURCES_MAPPING_FILE
from class_generator.core.schema import (
    ClusterVersionError,
    _convert_type_to_schema,
    _detect_missing_refs_from_schemas,
    _infer_oc_explain_path,
    build_dynamic_resource_to_api_mapping,
    build_namespacing_dict,
    check_and_update_cluster_version,
    extract_group_kind_version,
    fetch_all_api_schemas,
    find_api_paths_for_missing_resources,
    get_client_binary,
    get_server_version,
    identify_missing_resources,
    process_schema_definitions,
    read_resources_mapping_file,
    write_schema_files,
)


class TestGetClientBinary:
    """Test get_client_binary function."""

    @patch("class_generator.core.schema.run_command")
    def test_oc_binary_found(self, mock_run_command):
        """Test that oc binary is preferred when available."""
        mock_run_command.return_value = (True, "oc binary found", "")
        result = get_client_binary()
        assert result == "oc"

    @patch("class_generator.core.schema.run_command")
    def test_kubectl_binary_fallback(self, mock_run_command):
        """Test that kubectl is used when oc is not available."""
        mock_run_command.side_effect = [(False, "", "oc not found"), (True, "kubectl binary found", "")]
        result = get_client_binary()
        assert result == "kubectl"

    @patch("class_generator.core.schema.run_command")
    def test_no_binary_found_raises_error(self, mock_run_command):
        """Test that RuntimeError is raised when neither binary is found."""
        mock_run_command.return_value = (False, "", "binary not found")
        with pytest.raises(RuntimeError, match="Neither 'oc' nor 'kubectl' binary found"):
            get_client_binary()


class TestReadResourcesMappingFile:
    """Test read_resources_mapping_file function."""

    @patch("class_generator.core.schema.SchemaValidator")
    def test_successful_mapping_load(self, mock_schema_validator):
        """Test successful loading of resources mapping."""
        expected_mapping = {"pod": [{"kind": "Pod"}], "service": [{"kind": "Service"}]}
        mock_schema_validator.load_mappings_data.return_value = True
        mock_schema_validator.get_mappings_data.return_value = expected_mapping

        result = read_resources_mapping_file()
        assert result == expected_mapping

    @patch("class_generator.core.schema.SchemaValidator")
    def test_mapping_load_failure_returns_empty_dict(self, mock_schema_validator):
        """Test that empty dict is returned when mapping load fails."""
        mock_schema_validator.load_mappings_data.return_value = False

        result = read_resources_mapping_file()
        assert result == {}


class TestExtractGroupKindVersion:
    """Test extract_group_kind_version function."""

    def test_successful_extraction_with_group(self):
        """Test successful extraction when group is present."""
        kind_schema = {
            "x-kubernetes-group-version-kind": [
                {"group": "", "version": "v1", "kind": "Pod"},
                {"group": "apps", "version": "v1", "kind": "Deployment"},
            ]
        }
        result = extract_group_kind_version(kind_schema)
        assert result == {"group": "apps", "version": "v1", "kind": "Deployment"}

    def test_extraction_without_group_uses_first(self):
        """Test extraction uses first entry when all entries have empty/no group."""
        kind_schema = {"x-kubernetes-group-version-kind": [{"group": "", "version": "v1", "kind": "Pod"}]}
        result = extract_group_kind_version(kind_schema)
        assert result == {"group": "", "version": "v1", "kind": "Pod"}

    def test_extraction_prefers_entry_with_group(self):
        """Test extraction prefers first entry with non-empty group when multiple entries exist."""
        kind_schema = {
            "x-kubernetes-group-version-kind": [
                {"group": "", "version": "v1", "kind": "Pod"},  # First but empty group
                {"group": "apps", "version": "v1", "kind": "Deployment"},  # Should be selected
                {"group": "batch", "version": "v1", "kind": "Job"},  # Later entry, should be ignored
            ]
        }
        result = extract_group_kind_version(kind_schema)
        assert result == {"group": "apps", "version": "v1", "kind": "Deployment"}

    def test_extraction_multiple_entries_no_group_uses_last(self):
        """Test extraction uses last entry when multiple entries but none have groups."""
        kind_schema = {
            "x-kubernetes-group-version-kind": [
                {"group": "", "version": "v1", "kind": "Pod"},  # Should be ignored
                {"group": "", "version": "v2", "kind": "Pod"},  # Should be selected (last)
            ]
        }
        result = extract_group_kind_version(kind_schema)
        assert result == {"group": "", "version": "v2", "kind": "Pod"}

    def test_missing_key_raises_keyerror(self):
        """Test that KeyError is raised when required key is missing."""
        kind_schema = {"other_key": "value"}
        with pytest.raises(KeyError, match="Required key 'x-kubernetes-group-version-kind' not found"):
            extract_group_kind_version(kind_schema)

    def test_empty_list_raises_valueerror(self):
        """Test that ValueError is raised when list is empty."""
        kind_schema = {"x-kubernetes-group-version-kind": []}
        with pytest.raises(ValueError, match="x-kubernetes-group-version-kind list is empty"):
            extract_group_kind_version(kind_schema)


class TestGetServerVersion:
    """Test get_server_version function."""

    @patch("class_generator.core.schema.run_command")
    def test_successful_version_extraction(self, mock_run_command):
        """Test successful server version extraction."""
        version_output = {"clientVersion": {"gitVersion": "v1.29.0"}, "serverVersion": {"gitVersion": "v1.28.2+abc123"}}
        mock_run_command.return_value = (True, json.dumps(version_output), "")

        result = get_server_version("oc")
        assert result == "v1.28.2+abc123"

    @patch("class_generator.core.schema.run_command")
    def test_version_command_failure_raises_error(self, mock_run_command):
        """Test that RuntimeError is raised when version command fails."""
        mock_run_command.return_value = (False, "", "command failed")

        with pytest.raises(RuntimeError, match="Failed to get server version"):
            get_server_version("oc")


class TestBuildNamespacingDict:
    """Test build_namespacing_dict function."""

    @patch("class_generator.core.schema.run_command")
    def test_successful_namespacing_dict_build(self, mock_run_command):
        """Test successful building of namespacing dictionary."""
        namespaced_output = "pods                          po           v1                    Pod\nservices                      svc          v1                    Service"
        cluster_output = "nodes                         no           v1                    Node\nnamespaces                    ns           v1                    Namespace"

        mock_run_command.side_effect = [(True, namespaced_output, ""), (True, cluster_output, "")]

        result = build_namespacing_dict("kubectl")
        expected = {"Pod": True, "Service": True, "Node": False, "Namespace": False}
        assert result == expected

    @patch("class_generator.core.schema.run_command")
    def test_empty_output_handled_gracefully(self, mock_run_command):
        """Test that empty outputs are handled gracefully."""
        mock_run_command.side_effect = [(True, "", ""), (False, "", "")]

        result = build_namespacing_dict("kubectl")
        assert result == {}

    @patch("class_generator.core.schema.run_command")
    def test_malformed_lines_ignored(self, mock_run_command):
        """Test that malformed lines are ignored."""
        malformed_output = "pods                          po           v1                    Pod\n\n   \nservices                      svc          v1                    Service"

        mock_run_command.side_effect = [(True, malformed_output, ""), (True, "", "")]

        result = build_namespacing_dict("kubectl")
        expected = {"Pod": True, "Service": True}
        assert result == expected


class TestCheckAndUpdateClusterVersion:
    """Test check_and_update_cluster_version function."""

    @patch("class_generator.core.schema.get_server_version")
    @patch("builtins.open", create=True)
    def test_newer_version_updates_file(self, mock_open, mock_get_server_version):
        """Test that newer cluster version updates the file."""
        mock_file = Mock()
        mock_open.return_value.__enter__.return_value = mock_file
        mock_file.read.return_value = "v1.27.0"
        mock_get_server_version.return_value = "v1.28.0+abc123"

        result = check_and_update_cluster_version("oc")
        assert result is True

        # Verify that the file was opened for writing
        assert mock_open.call_count == 2  # Once for reading, once for writing
        # Check both positional and keyword arguments for mode
        write_calls = [
            call
            for call in mock_open.call_args_list
            if (len(call[0]) > 1 and call[0][1] == "w") or call[1].get("mode") == "w"
        ]
        assert len(write_calls) == 1, "File should be opened for writing exactly once"

        # Verify that the correct cluster version file path is used
        expected_path = Path("class_generator/schema/__cluster_version__.txt")
        # Read calls either have no mode (defaults to 'r') or explicitly 'r'
        read_calls = [
            call
            for call in mock_open.call_args_list
            if (len(call[0]) == 1) or (len(call[0]) > 1 and call[0][1] == "r") or call[1].get("mode") == "r"
        ]
        assert len(read_calls) == 1, "File should be opened for reading exactly once"
        # Check that the file path used matches expected cluster version file
        assert str(expected_path) in str(read_calls[0][0][0]) or expected_path.name in str(read_calls[0][0][0])

        # Verify that write() was called on the file handle with the new version
        mock_file.write.assert_called_once_with("v1.28.0")

    @patch("class_generator.core.schema.get_server_version")
    @patch("builtins.open", create=True)
    def test_older_version_no_update(self, mock_open, mock_get_server_version):
        """Test that older cluster version doesn't update the file."""
        mock_file = Mock()
        mock_open.return_value.__enter__.return_value = mock_file
        mock_file.read.return_value = "v1.29.0"
        mock_get_server_version.return_value = "v1.28.0"

        result = check_and_update_cluster_version("oc")
        assert result is False

        # Verify that the file was only opened for reading, not writing
        assert mock_open.call_count == 1  # Only once for reading
        # Read calls either have no mode (defaults to 'r') or explicitly 'r'
        read_calls = [
            call
            for call in mock_open.call_args_list
            if (len(call[0]) == 1) or (len(call[0]) > 1 and call[0][1] == "r") or call[1].get("mode") == "r"
        ]
        assert len(read_calls) == 1, "File should be opened for reading exactly once"

        # Verify that write() was never called
        mock_file.write.assert_not_called()

    @patch("class_generator.core.schema.get_server_version")
    @patch("builtins.open", create=True)
    def test_same_version_updates_file(self, mock_open, mock_get_server_version):
        """Test that same cluster version updates the file and write is called."""
        mock_file = Mock()
        mock_open.return_value.__enter__.return_value = mock_file
        mock_file.read.return_value = "v1.28.0"
        mock_get_server_version.return_value = "v1.28.0+abc123"

        result = check_and_update_cluster_version("oc")
        assert result is True

        # Verify that the file was opened for both reading and writing
        assert mock_open.call_count == 2  # Once for reading, once for writing
        # Check both positional and keyword arguments for mode
        write_calls = [
            call
            for call in mock_open.call_args_list
            if (len(call[0]) > 1 and call[0][1] == "w") or call[1].get("mode") == "w"
        ]
        assert len(write_calls) == 1, "File should be opened for writing exactly once"

        # Verify that the correct cluster version file path is used
        expected_path = Path("class_generator/schema/__cluster_version__.txt")
        # Read calls either have no mode (defaults to 'r') or explicitly 'r'
        read_calls = [
            call
            for call in mock_open.call_args_list
            if (len(call[0]) == 1) or (len(call[0]) > 1 and call[0][1] == "r") or call[1].get("mode") == "r"
        ]
        assert len(read_calls) == 1, "File should be opened for reading exactly once"
        # Check that the file path used matches expected cluster version file
        assert str(expected_path) in str(read_calls[0][0][0]) or expected_path.name in str(read_calls[0][0][0])

        # Verify that write() was called with the cleaned version (without build suffix)
        mock_file.write.assert_called_once_with("v1.28.0")

    @patch("class_generator.core.schema.get_server_version")
    @patch("builtins.open", side_effect=FileNotFoundError("File not found"))
    def test_missing_file_raises_cluster_version_error(self, mock_open, mock_get_server_version):
        """Test that server version failure raises ClusterVersionError."""
        mock_get_server_version.side_effect = RuntimeError("Failed to get server version")

        with pytest.raises(ClusterVersionError, match="Failed to determine cluster version from server"):
            check_and_update_cluster_version("oc")


class TestIdentifyMissingResources:
    """Test identify_missing_resources function."""

    @patch("class_generator.core.schema.run_command")
    def test_successful_missing_resources_identification(self, mock_run_command):
        """Test successful identification of missing resources."""
        api_resources_output = """pods                          po           v1                    Pod
services                      svc          v1                    Service
deployments                   deploy       apps/v1               Deployment
configmaps                    cm           v1                    ConfigMap"""

        mock_run_command.return_value = (True, api_resources_output, "")

        existing_mapping = {
            "pod": [{"x-kubernetes-group-version-kind": [{"kind": "Pod"}]}],
            "service": [{"x-kubernetes-group-version-kind": [{"kind": "Service"}]}],
        }

        result = identify_missing_resources("kubectl", existing_mapping)
        expected = {"Deployment", "ConfigMap"}
        assert result == expected

    @patch("class_generator.core.schema.run_command")
    def test_api_resources_command_failure(self, mock_run_command):
        """Test handling when api-resources command fails."""
        mock_run_command.return_value = (False, "", "command failed")

        result = identify_missing_resources("kubectl", {})
        assert result == set()

    @patch("class_generator.core.schema.run_command")
    def test_no_missing_resources(self, mock_run_command):
        """Test when no resources are missing."""
        api_resources_output = """pods                          po           v1                    Pod
services                      svc          v1                    Service"""

        mock_run_command.return_value = (True, api_resources_output, "")

        existing_mapping = {
            "pod": [{"x-kubernetes-group-version-kind": [{"kind": "Pod"}]}],
            "service": [{"x-kubernetes-group-version-kind": [{"kind": "Service"}]}],
        }

        result = identify_missing_resources("kubectl", existing_mapping)
        assert result == set()

    @patch("class_generator.core.schema.run_command")
    def test_malformed_existing_mapping_handled(self, mock_run_command):
        """Test that malformed existing mapping is handled gracefully."""
        api_resources_output = "pods                          po           v1                    Pod"
        mock_run_command.return_value = (True, api_resources_output, "")

        # Malformed mapping - missing required structure
        malformed_mapping = {"invalid": "not_a_list", "empty": [], "missing_gvk": [{"no-gvk-key": "value"}]}

        result = identify_missing_resources("kubectl", malformed_mapping)
        assert "Pod" in result


class TestBuildDynamicResourceToApiMapping:
    """Test build_dynamic_resource_to_api_mapping function."""

    @patch("class_generator.core.schema.run_command")
    def test_successful_dynamic_mapping_build(self, mock_run_command):
        """Test successful building of dynamic resource-to-API mapping."""
        api_resources_output = """pods                          po           v1                         true         Pod                                  create,delete,deletecollection,get,list,patch,update,watch   all
services                      svc          v1                         true         Service                              create,delete,deletecollection,get,list,patch,update,watch   all
deployments                   deploy       apps/v1                    true         Deployment                           create,delete,deletecollection,get,list,patch,update,watch   all
jobs                                       batch/v1                   true         Job                                  create,delete,deletecollection,get,list,patch,update,watch
routes                                     route.openshift.io/v1      true         Route                                create,delete,deletecollection,get,list,patch,update,watch   """

        mock_run_command.return_value = (True, api_resources_output, "")

        result = build_dynamic_resource_to_api_mapping("kubectl")

        expected_mapping = {
            "Pod": ["api/v1"],
            "Service": ["api/v1"],
            "Deployment": ["apis/apps/v1"],
            "Job": ["apis/batch/v1"],
            "Route": ["apis/route.openshift.io/v1"],
        }
        assert result == expected_mapping

    @patch("class_generator.core.schema.run_command")
    def test_command_failure_returns_empty_mapping(self, mock_run_command):
        """Test that command failure returns empty mapping."""
        mock_run_command.return_value = (False, "", "command failed")

        result = build_dynamic_resource_to_api_mapping("kubectl")
        assert result == {}

    @patch("class_generator.core.schema.run_command")
    def test_empty_output_returns_empty_mapping(self, mock_run_command):
        """Test that empty output returns empty mapping."""
        mock_run_command.return_value = (True, "", "")

        result = build_dynamic_resource_to_api_mapping("kubectl")
        assert result == {}

    @patch("class_generator.core.schema.run_command")
    def test_malformed_lines_handled_gracefully(self, mock_run_command):
        """Test that malformed lines are handled gracefully."""
        api_resources_output = """pods                          po           v1                         true         Pod
incomplete_line
services                      svc          v1                         true         Service                              create,delete
short
"""
        mock_run_command.return_value = (True, api_resources_output, "")

        result = build_dynamic_resource_to_api_mapping("kubectl")
        # Should only include valid lines
        assert "Pod" in result
        assert "Service" in result
        assert len(result) == 2

    @patch("class_generator.core.schema.run_command")
    def test_core_v1_api_mapping(self, mock_run_command):
        """Test that core v1 API resources are mapped to api/v1."""
        api_resources_output = """pods                          po           v1                         true         Pod                                  create,delete,deletecollection,get,list,patch,update,watch   all
configmaps                    cm           v1                         true         ConfigMap                            create,delete,deletecollection,get,list,patch,update,watch
secrets                                    v1                         true         Secret                               create,delete,deletecollection,get,list,patch,update,watch   """

        mock_run_command.return_value = (True, api_resources_output, "")

        result = build_dynamic_resource_to_api_mapping("kubectl")

        # All v1 resources should map to api/v1
        assert result["Pod"] == ["api/v1"]
        assert result["ConfigMap"] == ["api/v1"]
        assert result["Secret"] == ["api/v1"]

    @patch("class_generator.core.schema.run_command")
    def test_apps_api_group_mapping(self, mock_run_command):
        """Test that apps API group resources are mapped correctly."""
        api_resources_output = """deployments                   deploy       apps/v1                    true         Deployment                           create,delete,deletecollection,get,list,patch,update,watch   all
replicasets                   rs           apps/v1                    true         ReplicaSet                           create,delete,deletecollection,get,list,patch,update,watch   all
statefulsets                  sts          apps/v1                    true         StatefulSet                          create,delete,deletecollection,get,list,patch,update,watch   all"""

        mock_run_command.return_value = (True, api_resources_output, "")

        result = build_dynamic_resource_to_api_mapping("kubectl")

        # All apps/v1 resources should map to apis/apps/v1
        assert result["Deployment"] == ["apis/apps/v1"]
        assert result["ReplicaSet"] == ["apis/apps/v1"]
        assert result["StatefulSet"] == ["apis/apps/v1"]

    @patch("class_generator.core.schema.run_command")
    def test_openshift_api_groups_mapping(self, mock_run_command):
        """Test that OpenShift API groups are mapped correctly."""
        api_resources_output = """routes                                     route.openshift.io/v1      true         Route                                create,delete,deletecollection,get,list,patch,update,watch
buildconfigs                  bc           build.openshift.io/v1      true         BuildConfig                          create,delete,deletecollection,get,list,patch,update,watch
clusterversions                            config.openshift.io/v1     false        ClusterVersion                       delete,deletecollection,get,list,patch,create,update,watch   """

        mock_run_command.return_value = (True, api_resources_output, "")

        result = build_dynamic_resource_to_api_mapping("kubectl")

        # OpenShift resources should map to their respective APIs
        assert result["Route"] == ["apis/route.openshift.io/v1"]
        assert result["BuildConfig"] == ["apis/build.openshift.io/v1"]
        assert result["ClusterVersion"] == ["apis/config.openshift.io/v1"]

    @patch("class_generator.core.schema.run_command")
    def test_multiple_versions_same_kind(self, mock_run_command):
        """Test that multiple API versions for same kind are handled."""
        api_resources_output = """ingresses                              networking.k8s.io/v1       true         Ingress                              create,delete,deletecollection,get,list,patch,update,watch
ingresses                              networking.k8s.io/v1beta1  true         Ingress                              create,delete,deletecollection,get,list,patch,update,watch   """

        mock_run_command.return_value = (True, api_resources_output, "")

        result = build_dynamic_resource_to_api_mapping("kubectl")

        # Should include both API versions
        assert len(result["Ingress"]) == 2
        assert "apis/networking.k8s.io/v1" in result["Ingress"]
        assert "apis/networking.k8s.io/v1beta1" in result["Ingress"]

    @patch("class_generator.core.schema.run_command")
    def test_variable_shortnames_column_handled(self, mock_run_command):
        """Test that variable SHORTNAMES column is handled correctly."""
        api_resources_output = """bindings                                                       v1                         true         Binding                              create
componentstatuses             cs                           v1                         false        ComponentStatus                      get,list
events                        ev                           v1                         true         Event                                create,delete,deletecollection,get,list,patch,update,watch
limitranges                   limits                       v1                         true         LimitRange                           create,delete,deletecollection,get,list,patch,update,watch   """

        mock_run_command.return_value = (True, api_resources_output, "")

        result = build_dynamic_resource_to_api_mapping("kubectl")

        # Should handle lines with and without shortnames correctly
        assert result["Binding"] == ["api/v1"]
        assert result["ComponentStatus"] == ["api/v1"]
        assert result["Event"] == ["api/v1"]
        assert result["LimitRange"] == ["api/v1"]

    @patch("class_generator.core.schema.run_command")
    def test_parsing_exception_handling(self, mock_run_command):
        """Test that parsing exceptions are handled gracefully."""
        # Create output that will cause parsing issues
        api_resources_output = """valid_line                    sc           v1                         true         ValidResource                        create,delete
invalid version format        sc           invalid                    true         InvalidResource                      create
missing_columns               sc
"""
        mock_run_command.return_value = (True, api_resources_output, "")

        result = build_dynamic_resource_to_api_mapping("kubectl")

        # Should only include resources that parsed successfully
        assert "ValidResource" in result
        assert "InvalidResource" not in result
        assert len(result) == 1

    @patch("class_generator.core.schema.run_command")
    def test_subresource_paths_included(self, mock_run_command):
        """Test that CRD with APIVERSION containing subresource path-like strings are included as separate kinds."""
        api_resources_output = """widgets                       widget       widgets.example.io/v1      true         Widget                               create,delete,deletecollection,get,list,patch,update,watch
widgets                       widget       widgets.example.io/v1      true         Widget/status                        create,delete
widgets                       widget       widgets.example.io/v1      true         Widget/spec                          create,update
customresources               cr           custom.io/v1               true         CustomResource                       create,delete,deletecollection,get,list,patch,update,watch
customresources/finalizers    cr           custom.io/v1               true         CustomResource/finalizers            update,patch"""

        mock_run_command.return_value = (True, api_resources_output, "")

        result = build_dynamic_resource_to_api_mapping("kubectl")

        # Should include both main resource kinds and subresource paths as separate kinds
        expected_mapping = {
            "Widget": ["apis/widgets.example.io/v1"],
            "Widget/status": ["apis/widgets.example.io/v1"],
            "Widget/spec": ["apis/widgets.example.io/v1"],
            "CustomResource": ["apis/custom.io/v1"],
            "CustomResource/finalizers": ["apis/custom.io/v1"],
        }
        assert result == expected_mapping

        # Verify subresource entries are included as separate keys (current behavior)
        assert "Widget/status" in result
        assert "Widget/spec" in result
        assert "CustomResource/finalizers" in result


class TestFindApiPathsForMissingResources:
    """Test find_api_paths_for_missing_resources function - updated to use dynamic discovery."""

    @patch("class_generator.core.schema.build_dynamic_resource_to_api_mapping")
    def test_dynamic_mapping_used(self, mock_build_mapping):
        """Test that dynamic mapping is used instead of hardcoded mapping."""
        mock_build_mapping.return_value = {
            "Pod": ["api/v1"],
            "Deployment": ["apis/apps/v1"],
            "CustomResource": ["apis/custom.io/v1"],
        }

        paths = {
            "api/v1": {"serverRelativeURL": "/api/v1"},
            "apis/apps/v1": {"serverRelativeURL": "/apis/apps/v1"},
            "apis/custom.io/v1": {"serverRelativeURL": "/apis/custom.io/v1"},
        }
        missing_resources = {"Pod", "CustomResource"}

        result = find_api_paths_for_missing_resources("kubectl", paths, missing_resources)

        # Should use dynamic mapping
        mock_build_mapping.assert_called_once_with("kubectl")
        expected = {"api/v1", "apis/custom.io/v1"}
        assert result == expected

    @patch("class_generator.core.schema.build_dynamic_resource_to_api_mapping")
    def test_fallback_to_hardcoded_mapping(self, mock_build_mapping):
        """Test fallback to hardcoded mapping when dynamic discovery fails."""
        mock_build_mapping.return_value = {}  # Empty mapping (failure)

        paths = {
            "api/v1": {"serverRelativeURL": "/api/v1"},
            "apis/apps/v1": {"serverRelativeURL": "/apis/apps/v1"},
        }
        missing_resources = {"Pod", "Deployment"}

        result = find_api_paths_for_missing_resources("kubectl", paths, missing_resources)

        # Should fall back to hardcoded mapping
        expected = {"api/v1", "apis/apps/v1"}
        assert result == expected

    def test_known_resources_mapping(self):
        """Test that known resources are mapped to correct API paths."""
        paths = {
            "api/v1": {"serverRelativeURL": "/api/v1"},
            "apis/apps/v1": {"serverRelativeURL": "/apis/apps/v1"},
            "apis/batch/v1": {"serverRelativeURL": "/apis/batch/v1"},
        }
        missing_resources = {"Pod", "Deployment", "Job"}

        # Mock the dynamic mapping to return expected results
        with patch("class_generator.core.schema.build_dynamic_resource_to_api_mapping") as mock_build:
            mock_build.return_value = {
                "Pod": ["api/v1"],
                "Deployment": ["apis/apps/v1"],
                "Job": ["apis/batch/v1"],
            }

            result = find_api_paths_for_missing_resources("kubectl", paths, missing_resources)
            expected = {"api/v1", "apis/apps/v1", "apis/batch/v1"}
            assert result == expected

    @patch("class_generator.core.schema.build_dynamic_resource_to_api_mapping")
    def test_unknown_resources_get_default_paths(self, mock_build_mapping):
        """Test that unknown resources get mapped to default OpenShift paths."""
        mock_build_mapping.return_value = {}  # Empty mapping for unknown resources

        paths = {
            "api/v1": {"serverRelativeURL": "/api/v1"},
            "apis/apps.openshift.io/v1": {"serverRelativeURL": "/apis/apps.openshift.io/v1"},
            "apis/config.openshift.io/v1": {"serverRelativeURL": "/apis/config.openshift.io/v1"},
        }
        missing_resources = {"UnknownResource"}

        result = find_api_paths_for_missing_resources("kubectl", paths, missing_resources)
        # Should include core API and OpenShift API groups for unknown resources
        assert "api/v1" in result
        assert "apis/apps.openshift.io/v1" in result

    def test_empty_missing_resources(self):
        """Test that empty missing resources returns empty set."""
        paths = {"api/v1": {"serverRelativeURL": "/api/v1"}}
        missing_resources = set()

        result = find_api_paths_for_missing_resources("kubectl", paths, missing_resources)
        assert result == set()

    @patch("class_generator.core.schema.build_dynamic_resource_to_api_mapping")
    def test_missing_api_paths_in_cluster(self, mock_build_mapping):
        """Test handling when expected API paths are not available in cluster."""
        mock_build_mapping.return_value = {"Deployment": ["apis/apps/v1"]}

        paths = {"api/v1": {"serverRelativeURL": "/api/v1"}}  # Missing apps/v1
        missing_resources = {"Deployment"}  # Deployment usually in apps/v1

        result = find_api_paths_for_missing_resources("kubectl", paths, missing_resources)
        # Should still return empty since apps/v1 not available
        assert result == set()

    @patch("class_generator.core.schema.build_dynamic_resource_to_api_mapping")
    def test_openshift_specific_resources(self, mock_build_mapping):
        """Test OpenShift-specific resources are mapped correctly."""
        mock_build_mapping.return_value = {
            "Route": ["apis/route.openshift.io/v1"],
            "BuildConfig": ["apis/build.openshift.io/v1"],
        }

        paths = {
            "apis/route.openshift.io/v1": {"serverRelativeURL": "/apis/route.openshift.io/v1"},
            "apis/build.openshift.io/v1": {"serverRelativeURL": "/apis/build.openshift.io/v1"},
        }
        missing_resources = {"Route", "BuildConfig"}

        result = find_api_paths_for_missing_resources("kubectl", paths, missing_resources)
        expected = {"apis/route.openshift.io/v1", "apis/build.openshift.io/v1"}
        assert result == expected

    @patch("class_generator.core.schema.build_dynamic_resource_to_api_mapping")
    def test_mixed_known_and_unknown_resources(self, mock_build_mapping):
        """Test mix of known and unknown resources."""
        mock_build_mapping.return_value = {"Pod": ["api/v1"]}  # Only Pod known

        paths = {
            "api/v1": {"serverRelativeURL": "/api/v1"},
            "apis/apps/v1": {"serverRelativeURL": "/apis/apps/v1"},
            "apis/apps.openshift.io/v1": {"serverRelativeURL": "/apis/apps.openshift.io/v1"},
        }
        missing_resources = {"Pod", "UnknownResource"}

        result = find_api_paths_for_missing_resources("kubectl", paths, missing_resources)
        # Should include api/v1 for Pod and default paths for unknown
        assert "api/v1" in result
        assert "apis/apps.openshift.io/v1" in result  # Default OpenShift path

    @patch("class_generator.core.schema.build_dynamic_resource_to_api_mapping")
    def test_uploadtokenrequest_special_case(self, mock_build_mapping):
        """Test UploadTokenRequest which could be in either api (using fallback)."""
        mock_build_mapping.return_value = {}  # Empty - force fallback to hardcoded

        paths = {
            "api/v1": {"serverRelativeURL": "/api/v1"},
            "apis/image.openshift.io/v1": {"serverRelativeURL": "/apis/image.openshift.io/v1"},
        }
        missing_resources = {"UploadTokenRequest"}

        result = find_api_paths_for_missing_resources("kubectl", paths, missing_resources)
        # Should check both API paths using fallback hardcoded mapping
        assert "api/v1" in result
        assert "apis/image.openshift.io/v1" in result


class TestFetchAllApiSchemas:
    """Test fetch_all_api_schemas function."""

    @patch("class_generator.core.schema.run_command")
    def test_successful_schema_fetching(self, mock_run_command):
        """Test successful fetching of API schemas."""
        schema_data = {"swagger": "2.0", "components": {"schemas": {}}}
        mock_run_command.return_value = (True, json.dumps(schema_data), "")

        paths = {"api/v1": {"serverRelativeURL": "/api/v1"}}
        result = fetch_all_api_schemas("kubectl", paths)

        assert isinstance(result, dict)
        assert "api/v1" in result

    @patch("class_generator.core.schema.run_command")
    def test_failed_schema_fetch_handled(self, mock_run_command):
        """Test that failed schema fetches are handled gracefully."""
        mock_run_command.return_value = (False, "", "fetch failed")

        paths = {"api/v1": {"serverRelativeURL": "/api/v1"}}
        result = fetch_all_api_schemas("kubectl", paths)

        assert result == {}

    @patch("class_generator.core.schema.run_command")
    def test_invalid_json_handled(self, mock_run_command):
        """Test that invalid JSON responses are handled gracefully."""
        mock_run_command.return_value = (True, "invalid json", "")

        paths = {"api/v1": {"serverRelativeURL": "/api/v1"}}
        result = fetch_all_api_schemas("kubectl", paths)

        assert result == {}

    @patch("class_generator.core.schema.run_command")
    def test_filter_paths_functionality(self, mock_run_command):
        """Test that filter_paths parameter works correctly."""
        schema_data = {"swagger": "2.0", "components": {"schemas": {}}}
        mock_run_command.return_value = (True, json.dumps(schema_data), "")

        paths = {"api/v1": {"serverRelativeURL": "/api/v1"}, "apis/apps/v1": {"serverRelativeURL": "/apis/apps/v1"}}
        filter_paths = {"api/v1"}

        result = fetch_all_api_schemas("kubectl", paths, filter_paths)
        # Should only process filtered paths - assert exactly the filter set to guard against over-fetching
        assert isinstance(result, dict)
        assert set(result.keys()) == filter_paths, f"Expected exactly {filter_paths}, got {set(result.keys())}"

    def test_filter_paths_validation_valid_set(self):
        """Test that valid filter_paths set passes validation."""
        paths = {"api/v1": {"serverRelativeURL": "/api/v1"}, "apis/apps/v1": {"serverRelativeURL": "/apis/apps/v1"}}
        filter_paths = {"api/v1", "apis/apps/v1"}

        # Should not raise any exception during validation
        with patch("class_generator.core.schema.run_command") as mock_run_command:
            mock_run_command.return_value = (True, '{"swagger": "2.0"}', "")
            result = fetch_all_api_schemas("kubectl", paths, filter_paths)
            assert isinstance(result, dict)
            # Assert that resulting keys are exactly the filter set to guard against over-fetching
            assert set(result.keys()) == filter_paths, f"Expected exactly {filter_paths}, got {set(result.keys())}"

    def test_filter_paths_validation_converts_iterable_to_set(self):
        """Test that filter_paths list is converted to set."""
        paths = {"api/v1": {"serverRelativeURL": "/api/v1"}, "apis/apps/v1": {"serverRelativeURL": "/apis/apps/v1"}}
        filter_paths = ["api/v1", "apis/apps/v1"]  # List instead of set

        # Should not raise any exception during validation
        with patch("class_generator.core.schema.run_command") as mock_run_command:
            mock_run_command.return_value = (True, '{"swagger": "2.0"}', "")
            result = fetch_all_api_schemas("kubectl", paths, filter_paths)
            assert isinstance(result, dict)
            # Assert that resulting keys are exactly the filter set to guard against over-fetching
            expected_keys = set(filter_paths)
            assert set(result.keys()) == expected_keys, f"Expected exactly {expected_keys}, got {set(result.keys())}"

    def test_filter_paths_validation_string_with_invalid_chars_raises_valueerror(self):
        """Test that string filter_paths with invalid characters raises ValueError."""
        paths = {"api/v1": {"serverRelativeURL": "/api/v1"}}
        filter_paths = "not_iterable"  # String is iterable but each char isn't a valid path

        with pytest.raises(ValueError) as exc_info:
            fetch_all_api_schemas("kubectl", paths, filter_paths)
        # Verify it's about missing paths without coupling to exact message
        assert "filter_paths" in str(exc_info.value)
        assert "not present" in str(exc_info.value) or "missing" in str(exc_info.value)

    def test_filter_paths_validation_non_iterable_type_raises_typeerror(self):
        """Test that non-iterable filter_paths type raises TypeError."""
        paths = {"api/v1": {"serverRelativeURL": "/api/v1"}}
        filter_paths = 123  # Not iterable

        with pytest.raises(TypeError) as exc_info:
            fetch_all_api_schemas("kubectl", paths, filter_paths)
        # Verify it's about type without coupling to exact message
        assert "filter_paths" in str(exc_info.value)
        assert "int" in str(exc_info.value)

    def test_filter_paths_validation_non_string_items_raises_typeerror(self):
        """Test that non-string items in filter_paths raise TypeError."""
        paths = {"api/v1": {"serverRelativeURL": "/api/v1"}}
        filter_paths = {"api/v1", 123, None}  # Mixed types

        with pytest.raises(TypeError) as exc_info:
            fetch_all_api_schemas("kubectl", paths, filter_paths)
        # Verify it's about invalid string items without coupling to exact message
        assert "filter_paths" in str(exc_info.value)
        assert "string" in str(exc_info.value)
        assert "invalid" in str(exc_info.value) or "items" in str(exc_info.value)

    def test_filter_paths_validation_empty_string_raises_typeerror(self):
        """Test that empty string in filter_paths raises TypeError."""
        paths = {"api/v1": {"serverRelativeURL": "/api/v1"}}
        filter_paths = {"api/v1", ""}  # Empty string

        with pytest.raises(TypeError) as exc_info:
            fetch_all_api_schemas("kubectl", paths, filter_paths)
        # Verify it's about empty strings without coupling to exact message
        assert "filter_paths" in str(exc_info.value)
        assert "string" in str(exc_info.value)
        assert "empty" in str(exc_info.value) or "non-empty" in str(exc_info.value)

    def test_filter_paths_validation_missing_paths_raises_valueerror(self):
        """Test that filter_paths not present in paths raise ValueError."""
        paths = {"api/v1": {"serverRelativeURL": "/api/v1"}}
        filter_paths = {"api/v1", "apis/missing/v1", "api/v2"}  # Some paths not in paths dict

        with pytest.raises(ValueError) as exc_info:
            fetch_all_api_schemas("kubectl", paths, filter_paths)
        # Verify it's about missing paths without coupling to exact message
        assert "filter_paths" in str(exc_info.value)
        assert "missing/v1" in str(exc_info.value)  # Specific missing path mentioned
        assert "api/v2" in str(exc_info.value)  # Another specific missing path mentioned

    def test_filter_paths_validation_missing_paths_includes_available_paths(self):
        """Test that ValueError includes available paths for debugging."""
        paths = {"api/v1": {"serverRelativeURL": "/api/v1"}, "apis/apps/v1": {"serverRelativeURL": "/apis/apps/v1"}}
        filter_paths = {"missing/path"}

        with pytest.raises(ValueError) as exc_info:
            fetch_all_api_schemas("kubectl", paths, filter_paths)

        error_message = str(exc_info.value)
        # Verify the essential information is present without exact wording
        assert "missing/path" in error_message
        assert "api/v1" in error_message  # Available path mentioned
        assert "apis/apps/v1" in error_message  # Another available path mentioned
        # Check for availability indicator (flexible wording)
        assert "available" in error_message.lower() or "paths" in error_message.lower()

    def test_filter_paths_none_allows_all_paths(self):
        """Test that filter_paths=None processes all paths (existing behavior)."""
        paths = {"api/v1": {"serverRelativeURL": "/api/v1"}, "apis/apps/v1": {"serverRelativeURL": "/apis/apps/v1"}}
        filter_paths = None

        with patch("class_generator.core.schema.run_command") as mock_run_command:
            mock_run_command.return_value = (True, '{"swagger": "2.0"}', "")
            result = fetch_all_api_schemas("kubectl", paths, filter_paths)
            assert isinstance(result, dict)


class TestProcessSchemaDefinitions:
    """Test process_schema_definitions function."""

    def test_process_new_resources(self):
        """Test processing schemas for new resources."""
        schemas = {
            "api/v1": {
                "components": {
                    "schemas": {
                        "io.k8s.api.core.v1.Pod": {
                            "type": "object",
                            "description": "Pod schema",
                            "properties": {"spec": {"type": "object"}},
                            "x-kubernetes-group-version-kind": [{"group": "", "version": "v1", "kind": "Pod"}],
                        }
                    }
                }
            }
        }
        namespacing_dict = {"Pod": True}
        existing_mapping = {}

        resources_mapping, definitions = process_schema_definitions(
            schemas, namespacing_dict, existing_mapping, allow_updates=True
        )

        assert "pod" in resources_mapping
        assert len(resources_mapping["pod"]) == 1
        assert resources_mapping["pod"][0]["namespaced"] is True
        assert "v1/Pod" in definitions

    def test_preserve_existing_resources_no_updates(self):
        """Test that existing resources are preserved when updates are not allowed."""
        schemas = {
            "api/v1": {
                "components": {
                    "schemas": {
                        "io.k8s.api.core.v1.Pod": {
                            "type": "object",
                            "x-kubernetes-group-version-kind": [{"group": "", "version": "v1", "kind": "Pod"}],
                        }
                    }
                }
            }
        }
        namespacing_dict = {"Pod": True}
        existing_mapping = {
            "pod": [{"x-kubernetes-group-version-kind": [{"group": "", "version": "v1", "kind": "Pod"}]}]
        }

        with patch("builtins.open", create=True) as mock_open:
            mock_file = Mock()
            mock_open.return_value.__enter__.return_value = mock_file
            mock_file.read.return_value = '{"definitions": {}}'

            resources_mapping, _definitions = process_schema_definitions(
                schemas, namespacing_dict, existing_mapping, allow_updates=False
            )

        # Should preserve existing resources
        assert "pod" in resources_mapping

    def test_skip_schemas_without_gvk(self):
        """Test that schemas without group-version-kind are skipped."""
        schemas = {
            "api/v1": {
                "components": {"schemas": {"InvalidSchema": {"type": "object", "description": "Schema without GVK"}}}
            }
        }
        namespacing_dict = {}
        existing_mapping = {}

        resources_mapping, definitions = process_schema_definitions(
            schemas, namespacing_dict, existing_mapping, allow_updates=True
        )

        # Should not add invalid schemas
        assert len(resources_mapping) == 0
        assert len(definitions) == 0

    def test_update_existing_resources_with_new_version(self):
        """Test updating existing resources with new API versions."""
        schemas = {
            "apis/apps/v1": {
                "components": {
                    "schemas": {
                        "io.k8s.api.apps.v1.Deployment": {
                            "type": "object",
                            "x-kubernetes-group-version-kind": [
                                {"group": "apps", "version": "v1", "kind": "Deployment"}
                            ],
                        }
                    }
                }
            }
        }
        namespacing_dict = {"Deployment": True}
        existing_mapping = {
            "deployment": [
                {"x-kubernetes-group-version-kind": [{"group": "apps", "version": "v1beta1", "kind": "Deployment"}]}
            ]
        }

        resources_mapping, _definitions = process_schema_definitions(
            schemas, namespacing_dict, existing_mapping, allow_updates=True
        )

        # Should add new version while preserving old
        assert "deployment" in resources_mapping
        assert len(resources_mapping["deployment"]) == 2  # Both versions


class TestWriteSchemaFiles:
    """Test write_schema_files function."""

    @patch("class_generator.core.schema.Path")
    @patch("class_generator.core.schema.save_json_archive")
    @patch("builtins.open", create=True)
    @patch("class_generator.core.schema._get_missing_core_definitions")
    @patch("class_generator.core.schema._supplement_schema_with_field_descriptions")
    def test_successful_file_writing(self, mock_supplement, mock_get_missing, mock_open, mock_save_archive, mock_path):
        """Test successful writing of schema files."""
        mock_path.return_value.mkdir = Mock()
        mock_file = Mock()
        mock_open.return_value.__enter__.return_value = mock_file
        mock_get_missing.return_value = {}
        mock_supplement.return_value = {"v1/Pod": {"type": "object"}}

        resources_mapping = {"pod": [{"kind": "Pod"}]}
        definitions = {"v1/Pod": {"type": "object"}}

        # No exception should be raised
        write_schema_files(resources_mapping, definitions, "kubectl")

        mock_save_archive.assert_called_once()

    @patch("class_generator.core.schema.Path")
    def test_directory_creation_failure(self, mock_path):
        """Test handling of directory creation failure."""
        mock_path.return_value.mkdir.side_effect = OSError("Permission denied")

        with pytest.raises(IOError, match="Failed to create schema directory"):
            write_schema_files({}, {}, "kubectl")

    @patch("class_generator.core.schema.Path")
    @patch("class_generator.core.schema._supplement_schema_with_field_descriptions")
    @patch("builtins.open", create=True)
    def test_file_writing_failure(self, mock_open, mock_supplement, mock_path):
        """Test handling of file writing failure."""
        mock_path.return_value.mkdir = Mock()
        mock_path.return_value.exists.return_value = False  # No existing file to preserve
        mock_open.side_effect = OSError("Write failed")
        mock_supplement.return_value = {"v1/Pod": {"type": "object"}}  # Return the same definitions

        # Use non-empty definitions to bypass the empty definitions guard
        non_empty_definitions = {"v1/Pod": {"type": "object"}}

        with pytest.raises(IOError, match="Failed to write definitions file"):
            write_schema_files({}, non_empty_definitions, "kubectl")

    @patch("class_generator.core.schema.Path")
    @patch("class_generator.core.schema.save_json_archive")
    @patch("builtins.open", create=True)
    @patch("class_generator.core.schema._get_missing_core_definitions")
    @patch("class_generator.core.schema._supplement_schema_with_field_descriptions")
    def test_empty_definitions_guard_preserves_existing_file(
        self, mock_supplement, mock_get_missing, mock_open, mock_save_archive, mock_path
    ):
        """Test that empty definitions don't overwrite existing definitions file."""
        # Setup mocks
        mock_path.return_value.mkdir = Mock()
        mock_path.return_value.exists.return_value = True  # Existing file exists
        mock_file = Mock()
        mock_open.return_value.__enter__.return_value = mock_file
        mock_get_missing.return_value = {}
        mock_supplement.return_value = {}

        resources_mapping = {"pod": [{"kind": "Pod"}]}
        empty_definitions = {}  # Empty definitions should trigger guard

        # Call the function
        write_schema_files(resources_mapping, empty_definitions, "kubectl", allow_supplementation=True)

        # Verify that missing definitions function is not called when no schemas provided
        mock_get_missing.assert_not_called()
        # Verify that supplementation is NOT called when no schemas and empty definitions
        mock_supplement.assert_not_called()

        # Verify that the definitions file is NOT opened for writing (guard protection)
        write_calls = [call for call in mock_open.call_args_list if len(call[0]) > 1 and call[0][1] == "w"]
        assert len(write_calls) == 0, "Definitions file should not be opened for writing when definitions are empty"

        # Verify that resources mapping is still saved (not affected by guard)
        # Assert the actual file path to ensure the correct mapping file is being saved
        mock_save_archive.assert_called_once_with(resources_mapping, RESOURCES_MAPPING_FILE)

    @patch("class_generator.core.schema.Path")
    @patch("class_generator.core.schema.save_json_archive")
    @patch("builtins.open", create=True)
    @patch("class_generator.core.schema._get_missing_core_definitions")
    @patch("class_generator.core.schema._supplement_schema_with_field_descriptions")
    def test_empty_definitions_guard_no_existing_file_still_writes(
        self, mock_supplement, mock_get_missing, mock_open, mock_save_archive, mock_path
    ):
        """Test that empty definitions still write when no existing file exists."""
        # Setup mocks
        mock_path.return_value.mkdir = Mock()
        mock_path.return_value.exists.return_value = False  # No existing file
        mock_file = Mock()
        mock_open.return_value.__enter__.return_value = mock_file
        mock_get_missing.return_value = {}
        mock_supplement.return_value = {}

        resources_mapping = {"pod": [{"kind": "Pod"}]}
        empty_definitions = {}  # Empty definitions

        # Call the function
        write_schema_files(resources_mapping, empty_definitions, "kubectl", allow_supplementation=True)

        # Verify that missing definitions function is not called when no schemas provided
        mock_get_missing.assert_not_called()
        # Verify that supplementation is NOT called when no schemas and empty definitions
        mock_supplement.assert_not_called()

        # Verify that the definitions file IS opened for writing when no existing file
        write_calls = [call for call in mock_open.call_args_list if len(call[0]) > 1 and call[0][1] == "w"]
        assert len(write_calls) == 1, "Definitions file should be opened for writing when no existing file"

        # Verify that resources mapping is saved
        # Assert the actual file path to ensure the correct mapping file is being saved
        mock_save_archive.assert_called_once_with(resources_mapping, RESOURCES_MAPPING_FILE)

    @patch("class_generator.core.schema.Path")
    @patch("class_generator.core.schema.save_json_archive")
    @patch("builtins.open", create=True)
    @patch("class_generator.core.schema._get_missing_core_definitions")
    @patch("class_generator.core.schema._supplement_schema_with_field_descriptions")
    def test_empty_definitions_guard_with_schemas_still_calls_enrichment(
        self, mock_supplement, mock_get_missing, mock_open, mock_save_archive, mock_path
    ):
        """Test that enrichment functions are called even with empty definitions when schemas provided."""
        # Setup mocks
        mock_path.return_value.mkdir = Mock()
        mock_path.return_value.exists.return_value = True  # Existing file exists
        mock_file = Mock()
        mock_open.return_value.__enter__.return_value = mock_file
        mock_get_missing.return_value = {"v1/NewDef": {"type": "object"}}  # Missing definitions found
        mock_supplement.return_value = {"v1/NewDef": {"type": "object"}}  # Supplementation adds content

        resources_mapping = {"pod": [{"kind": "Pod"}]}
        empty_definitions = {}  # Empty initial definitions
        schemas = {"api/v1": {"components": {"schemas": {}}}}  # Schemas provided

        # Call the function with schemas
        write_schema_files(resources_mapping, empty_definitions, "kubectl", schemas=schemas, allow_supplementation=True)

        # Verify that both enrichment functions are called
        mock_get_missing.assert_called_once_with(empty_definitions, "kubectl", schemas)
        mock_supplement.assert_called_once()

        # Since enrichment added content, file should be written
        write_calls = [call for call in mock_open.call_args_list if len(call[0]) > 1 and call[0][1] == "w"]
        assert len(write_calls) == 1, "Definitions file should be written when enrichment adds content"

        # Verify that resources mapping is saved
        # Assert the actual file path to ensure the correct mapping file is being saved
        mock_save_archive.assert_called_once_with(resources_mapping, RESOURCES_MAPPING_FILE)

    @patch("class_generator.core.schema.Path")
    @patch("class_generator.core.schema.save_json_archive")
    @patch("builtins.open", create=True)
    @patch("class_generator.core.schema._get_missing_core_definitions")
    @patch("class_generator.core.schema._supplement_schema_with_field_descriptions")
    def test_empty_definitions_guard_allows_supplementation_false(
        self, mock_supplement, mock_get_missing, mock_open, mock_save_archive, mock_path
    ):
        """Test that empty definitions guard works correctly when supplementation is disabled."""
        # Setup mocks
        mock_path.return_value.mkdir = Mock()
        mock_path.return_value.exists.return_value = True  # Existing file exists
        mock_file = Mock()
        mock_open.return_value.__enter__.return_value = mock_file
        mock_get_missing.return_value = {}
        # mock_supplement should not be called when allow_supplementation=False

        resources_mapping = {"pod": [{"kind": "Pod"}]}
        empty_definitions = {}  # Empty definitions

        # Call the function with supplementation disabled
        write_schema_files(resources_mapping, empty_definitions, "kubectl", allow_supplementation=False)

        # Verify that missing definitions function is still called when schemas provided
        # But since no schemas provided, it shouldn't be called
        mock_get_missing.assert_not_called()

        # Verify that supplementation is NOT called
        mock_supplement.assert_not_called()

        # Verify that the definitions file is NOT opened for writing (guard protection)
        write_calls = [call for call in mock_open.call_args_list if len(call[0]) > 1 and call[0][1] == "w"]
        assert len(write_calls) == 0, "Definitions file should not be opened for writing when definitions are empty"

        # Verify that resources mapping is still saved
        # Assert the actual file path to ensure the correct mapping file is being saved
        mock_save_archive.assert_called_once_with(resources_mapping, RESOURCES_MAPPING_FILE)

    @patch("class_generator.core.schema.Path")
    @patch("class_generator.core.schema.save_json_archive")
    @patch("builtins.open", create=True)
    @patch("class_generator.core.schema._get_missing_core_definitions")
    @patch("class_generator.core.schema._supplement_schema_with_field_descriptions")
    def test_empty_definitions_with_missing_definitions_from_enrichment(
        self, mock_supplement, mock_get_missing, mock_open, mock_save_archive, mock_path
    ):
        """Test that empty definitions get written when enrichment adds missing definitions."""
        # Setup mocks
        mock_path.return_value.mkdir = Mock()
        mock_path.return_value.exists.return_value = True  # Existing file exists
        mock_file = Mock()
        mock_open.return_value.__enter__.return_value = mock_file

        # Simulate enrichment functions adding content to empty definitions
        missing_definitions = {"v1/CoreDef": {"type": "object"}}
        supplemented_definitions = {"v1/CoreDef": {"type": "object", "description": "Added by supplementation"}}

        mock_get_missing.return_value = missing_definitions
        mock_supplement.return_value = supplemented_definitions

        resources_mapping = {"pod": [{"kind": "Pod"}]}
        empty_definitions = {}  # Start with empty definitions
        schemas = {"api/v1": {"components": {"schemas": {}}}}  # Provide schemas to trigger missing definitions check

        # Call the function
        write_schema_files(resources_mapping, empty_definitions, "kubectl", schemas=schemas, allow_supplementation=True)

        # Verify enrichment functions called
        mock_get_missing.assert_called_once_with(empty_definitions, "kubectl", schemas)
        mock_supplement.assert_called_once_with(missing_definitions, "kubectl")

        # Since enrichment added content, definitions file should be written
        write_calls = [call for call in mock_open.call_args_list if len(call[0]) > 1 and call[0][1] == "w"]
        assert len(write_calls) == 1, (
            "Definitions file should be written when enrichment adds content to initially empty definitions"
        )

        # Verify correct content written
        mock_file.write.assert_called()
        # The content is written as JSON with the definitions wrapped in a "definitions" object
        all_write_calls = [call[0][0] for call in mock_file.write.call_args_list]
        written_content = "".join(all_write_calls)

        # Parse the JSON and verify structure properly
        written_json = json.loads(written_content)
        assert "definitions" in written_json
        assert "v1/CoreDef" in written_json["definitions"]
        assert written_json["definitions"]["v1/CoreDef"]["type"] == "object"
        assert written_json["definitions"]["v1/CoreDef"]["description"] == "Added by supplementation"

        # Verify that resources mapping is saved
        # Assert the actual file path to ensure the correct mapping file is being saved
        mock_save_archive.assert_called_once_with(resources_mapping, RESOURCES_MAPPING_FILE)


class TestDetectMissingRefsFromSchemas:
    """Test _detect_missing_refs_from_schemas function."""

    def test_detect_missing_refs(self):
        """Test detection of missing reference definitions."""
        schemas = {
            "api/v1": {
                "components": {
                    "schemas": {
                        "Pod": {"properties": {"spec": {"$ref": "#/components/schemas/io.k8s.api.core.v1.PodSpec"}}}
                    }
                }
            }
        }
        definitions = {}

        result = _detect_missing_refs_from_schemas(schemas, definitions)
        assert "io.k8s.api.core.v1.PodSpec" in result

    def test_no_missing_refs_when_definitions_exist(self):
        """Test no missing refs when definitions already exist."""
        schemas = {
            "api/v1": {
                "components": {
                    "schemas": {
                        "Pod": {"properties": {"spec": {"$ref": "#/components/schemas/io.k8s.api.core.v1.PodSpec"}}}
                    }
                }
            }
        }
        definitions = {"io.k8s.api.core.v1.PodSpec": {"type": "object"}}

        result = _detect_missing_refs_from_schemas(schemas, definitions)
        assert len(result) == 0

    def test_refs_in_nested_structures(self):
        """Test detection of refs in nested structures."""
        schemas = {
            "api/v1": {
                "components": {
                    "schemas": {
                        "Pod": {
                            "properties": {
                                "spec": {
                                    "type": "object",
                                    "properties": {
                                        "containers": {
                                            "type": "array",
                                            "items": {"$ref": "#/components/schemas/io.k8s.api.core.v1.Container"},
                                        }
                                    },
                                }
                            }
                        }
                    }
                }
            }
        }
        definitions = {}

        result = _detect_missing_refs_from_schemas(schemas, definitions)
        assert "io.k8s.api.core.v1.Container" in result

    def test_circular_reference_detection(self):
        """Test that circular references don't cause infinite recursion."""
        # Create a circular reference structure
        obj_a = {"name": "ObjectA"}
        obj_b = {"name": "ObjectB"}
        obj_c = {"name": "ObjectC"}

        # Create circular references: A -> B -> C -> A
        obj_a["ref_to_b"] = obj_b
        obj_b["ref_to_c"] = obj_c
        obj_c["ref_to_a"] = obj_a

        # Add some $ref references to test the actual functionality
        obj_a["$ref"] = "#/definitions/MissingRef1"
        obj_b["$ref"] = "#/definitions/MissingRef2"

        schemas = {"api/v1": {"components": {"schemas": {"CircularTest": obj_a}}}}

        definitions = {}

        # This should not cause infinite recursion
        result = _detect_missing_refs_from_schemas(schemas, definitions)

        # Should detect the missing references
        assert "MissingRef1" in result
        assert "MissingRef2" in result
        assert len(result) == 2

    def test_self_referencing_object(self):
        """Test that an object referencing itself doesn't cause infinite recursion."""
        # Create a self-referencing object
        self_ref_obj = {"name": "SelfRef", "$ref": "#/definitions/MissingSelfRef"}
        self_ref_obj["self"] = self_ref_obj  # Self-reference

        schemas = {"api/v1": {"components": {"schemas": {"SelfRefTest": self_ref_obj}}}}

        definitions = {}

        # This should not cause infinite recursion
        result = _detect_missing_refs_from_schemas(schemas, definitions)

        # Should detect the missing reference
        assert "MissingSelfRef" in result
        assert len(result) == 1


class TestInferOcExplainPath:
    """Test _infer_oc_explain_path function."""

    @pytest.mark.parametrize(
        "ref,expected_path",
        [
            ("io.k8s.api.core.v1.PodSpec", "pod.spec"),
            ("io.k8s.api.apps.v1.DeploymentStatus", "deployment.status"),
            ("io.k8s.apimachinery.pkg.apis.meta.v1.ObjectMeta", "pod.metadata"),
            ("io.k8s.apimachinery.pkg.apis.meta.v1.LabelSelector", "deployment.spec.selector"),
            ("io.k8s.api.core.v1.Container", "pod.spec.containers"),
            ("io.k8s.api.core.v1.Volume", "pod.spec.volumes"),
            ("io.k8s.api.core.v1.ContainerPort", "pod.spec.containers.ports"),
        ],
    )
    def test_infer_known_paths(self, ref, expected_path):
        """Test inferring paths for known Kubernetes types."""
        result = _infer_oc_explain_path(ref)
        assert result == expected_path

    @pytest.mark.parametrize(
        "ref",
        [
            "unknown.reference.Type",
            "com.example.api.v1.CustomType",
            "io.k8s.Type",  # Too short
        ],
    )
    def test_infer_invalid_refs_return_none(self, ref):
        """Test that invalid or unknown refs return None."""
        result = _infer_oc_explain_path(ref)
        assert result is None


class TestConvertTypeToSchema:
    """Test _convert_type_to_schema function."""

    @pytest.mark.parametrize(
        "input_type,expected_schema",
        [
            # Basic types
            ("string", {"type": "string"}),
            ("integer", {"type": "integer"}),
            ("boolean", {"type": "boolean"}),
            ("number", {"type": "number"}),
            # Array types
            ("[]string", {"type": "array", "items": {"type": "string"}}),
            ("[]Container", {"type": "array", "items": {"type": "object"}}),
            # Map types
            ("map[string]string", {"type": "object"}),
            ("map[string]int", {"type": "object"}),
            # Complex/unknown types
            ("PodSpec", {"type": "object"}),
            ("CustomType", {"type": "object"}),
            # Edge cases
            ("", {"type": "object"}),
            # Nested array types
            ("[][]string", {"type": "array", "items": {"type": "array", "items": {"type": "string"}}}),
        ],
    )
    def test_convert_type_to_schema(self, input_type, expected_schema):
        """Test conversion of various types to schema format."""
        result = _convert_type_to_schema(input_type)
        assert result == expected_schema
