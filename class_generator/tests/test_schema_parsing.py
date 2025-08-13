"""Tests for schema parsing functions."""

from class_generator.core.schema import _clean_description, _parse_oc_explain_output


class TestCleanDescription:
    """Test the _clean_description function for cleaning kubectl explain output."""

    def test_simple_description_unchanged(self):
        """Test that simple descriptions remain unchanged."""
        simple_desc = ["This is a simple description about a field."]
        result = _clean_description(simple_desc)
        expected = "This is a simple description about a field."
        assert result == expected

    def test_technical_artifacts_removed(self):
        """Test that technical artifacts like <type> and -required- are removed."""
        polluted_desc = [
            "containers\t<[]Container> -required-",
            "List of containers belonging to the pod. Containers cannot currently be",
            "added or removed. There must be at least one container in a Pod.",
        ]
        result = _clean_description(polluted_desc)
        expected = "containers List of containers belonging to the pod. Containers cannot currently be added or removed. There must be at least one container in a Pod."
        assert result == expected

    def test_enum_values_section_removed(self):
        """Test that 'Possible enum values:' sections are removed."""
        enum_desc = [
            'Set DNS policy for the pod. Defaults to "ClusterFirst".',
            "",
            "Possible enum values:",
            ' - `"ClusterFirst"` indicates that the pod should use cluster DNS first',
            ' - `"ClusterFirstWithHostNet"` indicates that the pod should use cluster DNS',
        ]
        result = _clean_description(enum_desc)
        expected = 'Set DNS policy for the pod. Defaults to "ClusterFirst".'
        assert result == expected

    def test_bullet_points_removed(self):
        """Test that bullet point enum descriptions are removed."""
        bullet_desc = [
            "PreemptionPolicy is the Policy for preempting pods.",
            '- `"Never"` means that pod never preempts other pods with lower priority.',
            '- `"PreemptLowerPriority"` means that pod can preempt other pods.',
        ]
        result = _clean_description(bullet_desc)
        expected = "PreemptionPolicy is the Policy for preempting pods."
        assert result == expected

    def test_multiple_spaces_normalized(self):
        """Test that multiple consecutive spaces are normalized to single spaces."""
        spaced_desc = ["This    has    multiple      spaces   between    words."]
        result = _clean_description(spaced_desc)
        expected = "This has multiple spaces between words."
        assert result == expected

    def test_short_descriptions_filtered_out(self):
        """Test that very short descriptions are filtered out."""
        short_desc = ["val"]
        result = _clean_description(short_desc)
        assert result == ""

    def test_empty_description_list(self):
        """Test that empty description list returns empty string."""
        empty_desc = []
        result = _clean_description(empty_desc)
        assert result == ""

    def test_period_added_to_end(self):
        """Test that descriptions without periods get one added."""
        no_period_desc = ["This description has no period"]
        result = _clean_description(no_period_desc)
        expected = "This description has no period."
        assert result == expected

    def test_existing_period_preserved(self):
        """Test that existing periods are preserved."""
        with_period_desc = ["This description already has a period."]
        result = _clean_description(with_period_desc)
        expected = "This description already has a period."
        assert result == expected

    def test_complex_polluted_description(self):
        """Test cleaning a complex, heavily polluted description."""
        complex_desc = [
            "nodeAffinity\t<NodeAffinity> preferredDuringSchedulingIgnoredDuringExecution\t<[]PreferredSchedulingTerm>",
            "preference\t<NodeSelectorTerm> -required- matchExpressions\t<[]NodeSelectorRequirement>",
            "key\t<string> -required- operator\t<string> -required- values\t<[]string>",
        ]
        result = _clean_description(complex_desc)
        expected = "nodeAffinity preferredDuringSchedulingIgnoredDuringExecution preference matchExpressions key operator values."
        assert result == expected


class TestParseOcExplainOutput:
    """Test the _parse_oc_explain_output function for parsing kubectl explain output."""

    def test_basic_field_parsing(self):
        """Test that basic field information is parsed correctly."""
        sample_output = """KIND:       Pod
VERSION:    v1

FIELD: spec <PodSpec>

DESCRIPTION:
    Specification of the desired behavior of the pod.

FIELDS:
  activeDeadlineSeconds	<integer>
    Optional duration in seconds the pod may be active on the node.

  containers	<[]Container> -required-
    List of containers belonging to the pod. Cannot be updated.

  hostname	<string>
    Specifies the hostname of the Pod.
"""

        result = _parse_oc_explain_output(sample_output)

        assert result["type"] == "object"
        assert len(result["properties"]) == 3
        assert len(result["required"]) == 1

        # Check required field
        assert "containers" in result["required"]

        # Check field types
        assert result["properties"]["activeDeadlineSeconds"]["type"] == "integer"
        assert result["properties"]["containers"]["type"] == "array"
        assert result["properties"]["hostname"]["type"] == "string"

        # Check descriptions are cleaned
        active_desc = result["properties"]["activeDeadlineSeconds"]["description"]
        assert "Optional duration in seconds" in active_desc
        assert "<integer>" not in active_desc

        containers_desc = result["properties"]["containers"]["description"]
        assert "List of containers" in containers_desc
        assert "<[]Container>" not in containers_desc
        assert "-required-" not in containers_desc

    def test_empty_fields_section(self):
        """Test parsing output with no FIELDS section."""
        sample_output = """KIND:       Pod
VERSION:    v1

FIELD: spec <PodSpec>

DESCRIPTION:
    Specification of the desired behavior of the pod.
"""

        result = _parse_oc_explain_output(sample_output)

        assert result["type"] == "object"
        assert len(result["properties"]) == 0
        assert len(result["required"]) == 0

    def test_fields_with_enum_values(self):
        """Test parsing fields that have enum values sections."""
        sample_output = """KIND:       Pod
VERSION:    v1

FIELDS:
  dnsPolicy	<string>
    Set DNS policy for the pod. Defaults to "ClusterFirst".

    Possible enum values:
     - `"ClusterFirst"` indicates that the pod should use cluster DNS first
     - `"ClusterFirstWithHostNet"` indicates cluster DNS with host network
"""

        result = _parse_oc_explain_output(sample_output)

        assert len(result["properties"]) == 1
        dns_desc = result["properties"]["dnsPolicy"]["description"]
        assert "Set DNS policy for the pod" in dns_desc
        assert "Possible enum values:" not in dns_desc
        assert '`"ClusterFirst"`' not in dns_desc

    def test_malformed_field_lines_ignored(self):
        """Test that malformed field lines are ignored gracefully."""
        sample_output = """KIND:       Pod
VERSION:    v1

FIELDS:
  validField	<string>
    This is a valid field.

  malformedLine without tab or brackets
    This should be ignored.

  anotherValidField	<integer>
    Another valid field.
"""

        result = _parse_oc_explain_output(sample_output)

        # Should only parse the valid fields
        assert len(result["properties"]) == 2
        assert "validField" in result["properties"]
        assert "anotherValidField" in result["properties"]
        assert "malformedLine" not in result["properties"]
