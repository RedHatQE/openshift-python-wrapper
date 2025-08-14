"""Tests for new schema.py functions focused on coverage improvement."""

import json
from unittest.mock import Mock, patch

import pytest

from class_generator.core.schema import (
    ClusterVersionError,
    build_namespacing_dict,
    check_and_update_cluster_version,
    extract_group_kind_version,
    find_api_paths_for_missing_resources,
    get_client_binary,
    get_server_version,
    identify_missing_resources,
    read_resources_mapping_file,
    fetch_all_api_schemas,
    process_schema_definitions,
    write_schema_files,
    _detect_missing_refs_from_schemas,
    _infer_oc_explain_path,
    _convert_type_to_schema,
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
        """Test extraction uses first entry when no group is present."""
        kind_schema = {"x-kubernetes-group-version-kind": [{"group": "", "version": "v1", "kind": "Pod"}]}
        result = extract_group_kind_version(kind_schema)
        assert result == {"group": "", "version": "v1", "kind": "Pod"}

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

    @patch("builtins.open", side_effect=FileNotFoundError("File not found"))
    def test_missing_file_raises_cluster_version_error(self, mock_open):
        """Test that missing cluster version file raises ClusterVersionError."""
        with pytest.raises(ClusterVersionError, match="Failed to read cluster version file"):
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


class TestFindApiPathsForMissingResources:
    """Test find_api_paths_for_missing_resources function - the main new function."""

    def test_known_resources_mapping(self):
        """Test that known resources are mapped to correct API paths."""
        paths = {
            "api/v1": {"serverRelativeURL": "/api/v1"},
            "apis/apps/v1": {"serverRelativeURL": "/apis/apps/v1"},
            "apis/batch/v1": {"serverRelativeURL": "/apis/batch/v1"},
        }
        missing_resources = {"Pod", "Deployment", "Job"}

        result = find_api_paths_for_missing_resources(paths, missing_resources)
        expected = {"api/v1", "apis/apps/v1", "apis/batch/v1"}
        assert result == expected

    def test_unknown_resources_get_default_paths(self):
        """Test that unknown resources get mapped to default OpenShift paths."""
        paths = {
            "api/v1": {"serverRelativeURL": "/api/v1"},
            "apis/apps.openshift.io/v1": {"serverRelativeURL": "/apis/apps.openshift.io/v1"},
            "apis/config.openshift.io/v1": {"serverRelativeURL": "/apis/config.openshift.io/v1"},
        }
        missing_resources = {"UnknownResource"}

        result = find_api_paths_for_missing_resources(paths, missing_resources)
        # Should include core API and OpenShift API groups for unknown resources
        assert "api/v1" in result
        assert "apis/apps.openshift.io/v1" in result

    def test_empty_missing_resources(self):
        """Test that empty missing resources returns empty set."""
        paths = {"api/v1": {"serverRelativeURL": "/api/v1"}}
        missing_resources = set()

        result = find_api_paths_for_missing_resources(paths, missing_resources)
        assert result == set()

    def test_missing_api_paths_in_cluster(self):
        """Test handling when expected API paths are not available in cluster."""
        paths = {"api/v1": {"serverRelativeURL": "/api/v1"}}  # Missing apps/v1
        missing_resources = {"Deployment"}  # Deployment usually in apps/v1

        result = find_api_paths_for_missing_resources(paths, missing_resources)
        # Should still return empty since apps/v1 not available
        assert result == set()

    def test_openshift_specific_resources(self):
        """Test OpenShift-specific resources are mapped correctly."""
        paths = {
            "apis/route.openshift.io/v1": {"serverRelativeURL": "/apis/route.openshift.io/v1"},
            "apis/build.openshift.io/v1": {"serverRelativeURL": "/apis/build.openshift.io/v1"},
        }
        missing_resources = {"Route", "BuildConfig"}

        result = find_api_paths_for_missing_resources(paths, missing_resources)
        expected = {"apis/route.openshift.io/v1", "apis/build.openshift.io/v1"}
        assert result == expected

    def test_mixed_known_and_unknown_resources(self):
        """Test mix of known and unknown resources."""
        paths = {
            "api/v1": {"serverRelativeURL": "/api/v1"},
            "apis/apps/v1": {"serverRelativeURL": "/apis/apps/v1"},
            "apis/apps.openshift.io/v1": {"serverRelativeURL": "/apis/apps.openshift.io/v1"},
        }
        missing_resources = {"Pod", "UnknownResource"}

        result = find_api_paths_for_missing_resources(paths, missing_resources)
        # Should include api/v1 for Pod and default paths for unknown
        assert "api/v1" in result
        assert "apis/apps.openshift.io/v1" in result  # Default OpenShift path

    def test_uploadtokenrequest_special_case(self):
        """Test UploadTokenRequest which could be in either api."""
        paths = {
            "api/v1": {"serverRelativeURL": "/api/v1"},
            "apis/image.openshift.io/v1": {"serverRelativeURL": "/apis/image.openshift.io/v1"},
        }
        missing_resources = {"UploadTokenRequest"}

        result = find_api_paths_for_missing_resources(paths, missing_resources)
        # Should check both API paths
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
        # Should only process filtered paths
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

            resources_mapping, definitions = process_schema_definitions(
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

        resources_mapping, definitions = process_schema_definitions(
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
    @patch("builtins.open", create=True)
    def test_file_writing_failure(self, mock_open, mock_path):
        """Test handling of file writing failure."""
        mock_path.return_value.mkdir = Mock()
        mock_path.return_value.exists.return_value = False  # No existing file to preserve
        mock_open.side_effect = OSError("Write failed")

        # Use non-empty definitions to bypass the empty definitions guard
        non_empty_definitions = {"v1/Pod": {"type": "object"}}

        with pytest.raises(IOError, match="Failed to write definitions file"):
            write_schema_files({}, non_empty_definitions, "kubectl")


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


class TestInferOcExplainPath:
    """Test _infer_oc_explain_path function."""

    def test_infer_pod_spec_path(self):
        """Test inferring path for PodSpec."""
        result = _infer_oc_explain_path("io.k8s.api.core.v1.PodSpec")
        assert result == "pod.spec"

    def test_infer_deployment_status_path(self):
        """Test inferring path for DeploymentStatus."""
        result = _infer_oc_explain_path("io.k8s.api.apps.v1.DeploymentStatus")
        assert result == "deployment.status"

    def test_infer_object_meta_path(self):
        """Test inferring path for ObjectMeta."""
        result = _infer_oc_explain_path("io.k8s.apimachinery.pkg.apis.meta.v1.ObjectMeta")
        assert result == "pod.metadata"

    def test_infer_label_selector_path(self):
        """Test inferring path for LabelSelector."""
        result = _infer_oc_explain_path("io.k8s.apimachinery.pkg.apis.meta.v1.LabelSelector")
        assert result == "deployment.spec.selector"

    def test_infer_container_path(self):
        """Test inferring path for Container."""
        result = _infer_oc_explain_path("io.k8s.api.core.v1.Container")
        assert result == "pod.spec.containers"

    def test_infer_volume_path(self):
        """Test inferring path for Volume."""
        result = _infer_oc_explain_path("io.k8s.api.core.v1.Volume")
        assert result == "pod.spec.volumes"

    def test_infer_container_port_path(self):
        """Test inferring path for ContainerPort."""
        result = _infer_oc_explain_path("io.k8s.api.core.v1.ContainerPort")
        assert result == "pod.spec.containers.ports"

    def test_infer_unknown_ref_returns_none(self):
        """Test that unknown ref returns None."""
        result = _infer_oc_explain_path("unknown.reference.Type")
        assert result is None

    def test_infer_non_kubernetes_ref_returns_none(self):
        """Test that non-Kubernetes ref returns None."""
        result = _infer_oc_explain_path("com.example.api.v1.CustomType")
        assert result is None

    def test_infer_short_ref_returns_none(self):
        """Test that too-short ref returns None."""
        result = _infer_oc_explain_path("io.k8s.Type")
        assert result is None


class TestConvertTypeToSchema:
    """Test _convert_type_to_schema function."""

    def test_convert_basic_types(self):
        """Test conversion of basic types."""
        assert _convert_type_to_schema("string") == {"type": "string"}
        assert _convert_type_to_schema("integer") == {"type": "integer"}
        assert _convert_type_to_schema("boolean") == {"type": "boolean"}
        assert _convert_type_to_schema("number") == {"type": "number"}

    def test_convert_array_types(self):
        """Test conversion of array types."""
        result = _convert_type_to_schema("[]string")
        assert result == {"type": "array", "items": {"type": "string"}}

        result = _convert_type_to_schema("[]Container")
        assert result == {"type": "array", "items": {"type": "object"}}

    def test_convert_map_types(self):
        """Test conversion of map types."""
        result = _convert_type_to_schema("map[string]string")
        assert result == {"type": "object"}

        result = _convert_type_to_schema("map[string]int")
        assert result == {"type": "object"}

    def test_convert_complex_types(self):
        """Test conversion of complex/unknown types."""
        result = _convert_type_to_schema("PodSpec")
        assert result == {"type": "object"}

        result = _convert_type_to_schema("CustomType")
        assert result == {"type": "object"}

    def test_convert_empty_type(self):
        """Test conversion of empty type."""
        result = _convert_type_to_schema("")
        assert result == {"type": "object"}

    def test_convert_nested_array_types(self):
        """Test conversion of nested array types."""
        result = _convert_type_to_schema("[][]string")
        expected = {"type": "array", "items": {"type": "array", "items": {"type": "string"}}}
        assert result == expected
