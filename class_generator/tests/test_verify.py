"""Tests for the --verify mode: verifying generated files without modifying them."""

import os
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

import class_generator.cli
from class_generator.cli import main
from class_generator.constants import VERIFY_TEMP_FILE_PREFIX
from class_generator.core.generator import class_generator as generate_resource_class
from class_generator.core.generator import generate_resource_file_from_dict
from class_generator.formatters.file_writer import _format_file, classify_drift, verify_rendered


class TestVerifyRendered:
    """Test verify_rendered function."""

    def test_matching_content_returns_none(self, tmp_path):
        target = tmp_path / "resource.py"
        target.write_text("content\n")
        with patch("class_generator.formatters.file_writer._format_file"):
            assert verify_rendered(filepath=str(target), output="content\n") is None

    def test_drifted_content_returns_categories(self, tmp_path):
        target = tmp_path / "resource.py"
        target.write_text("original content\n")
        with patch("class_generator.formatters.file_writer._format_file"):
            assert verify_rendered(filepath=str(target), output="generated content\n") is not None

    def test_missing_file_returns_category(self, tmp_path):
        with patch("class_generator.formatters.file_writer._format_file") as mock_format:
            assert verify_rendered(filepath=str(tmp_path / "missing.py"), output="content\n") == ["file does not exist"]
            mock_format.assert_not_called()

    def test_temp_file_removed_on_success(self, tmp_path):
        target = tmp_path / "resource.py"
        target.write_text("content\n")
        with patch("class_generator.formatters.file_writer._format_file"):
            verify_rendered(filepath=str(target), output="content\n")
        assert list(tmp_path.glob(f"{VERIFY_TEMP_FILE_PREFIX}_*.py")) == []

    def test_temp_file_removed_on_format_failure(self, tmp_path):
        target = tmp_path / "resource.py"
        target.write_text("content\n")

        def failing_format(filepath: str) -> None:
            raise RuntimeError("format failed")

        with patch("class_generator.formatters.file_writer._format_file", side_effect=failing_format):
            assert verify_rendered(filepath=str(target), output="content\n") == ["formatting failed"]
        assert list(tmp_path.glob(f"{VERIFY_TEMP_FILE_PREFIX}_*.py")) == []

    def test_target_file_never_modified(self, tmp_path):
        target = tmp_path / "resource.py"
        target.write_text("original content\n")
        with patch("class_generator.formatters.file_writer._format_file"):
            verify_rendered(filepath=str(target), output="generated content\n")
        assert target.read_text() == "original content\n"


class TestClassifyDrift:
    """Test drift classification."""

    def test_identical_content_no_categories(self):
        source = "class A:\n    pass\n"
        assert classify_drift(committed=source, rendered=source) == []

    def test_blank_lines_only(self):
        committed = "class A:\n    def x(self):\n        pass\n"
        rendered = "class A:\n\n    def x(self):\n        pass\n"
        assert classify_drift(committed=committed, rendered=rendered) == ["blank lines"]

    def test_docstring_change_only(self):
        committed = 'class A:\n    """old doc"""\n    def x(self):\n        pass\n'
        rendered = 'class A:\n    """new doc"""\n    def x(self):\n        pass\n'
        assert classify_drift(committed=committed, rendered=rendered) == ["docstring add", "docstring delete"]

    def test_docstring_deletion_only(self):
        committed = 'class A:\n    """old doc"""\n    def x(self):\n        pass\n'
        rendered = "class A:\n    def x(self):\n        pass\n"
        assert classify_drift(committed=committed, rendered=rendered) == ["docstring delete"]

    def test_code_and_signature_change(self):
        committed = "class A:\n    def __init__(self, a=None):\n        self.a = a\n"
        rendered = "class A:\n    def __init__(self, b=None):\n        self.b = b\n"
        # renamed param = removed + added -> breaking
        assert classify_drift(committed=committed, rendered=rendered) == [
            "breaking change",
            "code add",
            "code delete",
            "signature code add",
            "signature code remove",
        ]

    def test_signature_param_removed_is_breaking(self):
        committed = "class A:\n    def __init__(self, a=None, b=None):\n        self.a = a\n        self.b = b\n"
        rendered = "class A:\n    def __init__(self, a=None):\n        self.a = a\n"
        assert classify_drift(committed=committed, rendered=rendered) == [
            "breaking change",
            "code add",
            "code delete",
            "signature code remove",
        ]

    def test_signature_param_added_is_not_breaking(self):
        committed = "class A:\n    def __init__(self, a=None):\n        self.a = a\n"
        rendered = "class A:\n    def __init__(self, a=None, b=None):\n        self.a = a\n        self.b = b\n"
        assert classify_drift(committed=committed, rendered=rendered) == [
            "code add",
            "code delete",
            "signature code add",
        ]

    def test_all_params_vanished_marks_schema_incomplete(self):
        committed = "class A:\n    def __init__(self, a=None, b=None):\n        self.a = a\n        self.b = b\n"
        rendered = "class A:\n    def __init__(self, **kwargs):\n        pass\n"
        categories = classify_drift(committed=committed, rendered=rendered)
        # the removals are real breakage, and the cause is flagged separately
        assert "breaking change" in categories
        assert "signature code remove" in categories
        assert "schema incomplete" in categories

    def test_schema_incomplete_not_flagged_without_params(self):
        committed = "class A:\n    def __init__(self, **kwargs):\n        pass\n"
        rendered = "class A:\n    def __init__(self, **kwargs):\n        pass\n"
        assert classify_drift(committed=committed, rendered=rendered) == []

    def test_code_addition_without_signature_change(self):
        committed = "class A:\n    def __init__(self, a=None):\n        self.a = a\n"
        rendered = "class A:\n    def __init__(self, a=None):\n        self.a = a\n        self.b = 1\n"
        assert classify_drift(committed=committed, rendered=rendered) == ["code add"]


class TestVerifyKindNotInSchema:
    """A kind missing from the schema mapping must fail verification, not pass silently."""

    def test_verify_unknown_kind_raises(self):
        with pytest.raises(RuntimeError, match="not found"):
            generate_resource_class(kind="DefinitelyNotAKnownKind", verify=True, called_from_cli=False)


class TestGenerateResourceFileVerify:
    """Test verify mode in generate_resource_file_from_dict."""

    def _resource_dict(self) -> dict:
        return {
            "kind": "Pod",
            "api_group": "",
            "namespaced": True,
            "api_version": "v1",
            "required_props": [],
            "optional_props": [],
            "user_code_props": [],
            "prop_type": {},
            "functions": [],
        }

    def test_verify_match_returns_orig(self, tmp_path):
        target = tmp_path / "pod.py"
        target.write_text(
            "# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md\n\nclass Pod:\n    pass\n"
        )

        with patch("class_generator.core.generator.render_jinja_template", return_value="class Pod:\n    pass\n"):
            with patch("class_generator.core.generator.parse_user_code_from_file", return_value=("", "")):
                with patch("class_generator.core.generator.verify_rendered", return_value=None) as mock_verify:
                    orig, generated = generate_resource_file_from_dict(
                        resource_dict=self._resource_dict(),
                        verify=True,
                        output_dir=str(tmp_path),
                    )

        assert orig == str(target)
        assert generated == str(target)
        mock_verify.assert_called_once()
        # File was not modified
        assert "class Pod:" in target.read_text()

    def test_verify_drift_returns_categories(self, tmp_path):
        target = tmp_path / "pod.py"
        target.write_text("# hand-edited content\n")

        with patch("class_generator.core.generator.render_jinja_template", return_value="class Pod:\n    pass\n"):
            with patch("class_generator.core.generator.parse_user_code_from_file", return_value=("", "")):
                with patch("class_generator.core.generator.verify_rendered", return_value=["code delete"]):
                    orig, generated = generate_resource_file_from_dict(
                        resource_dict=self._resource_dict(),
                        verify=True,
                        output_dir=str(tmp_path),
                    )

        assert orig == str(target)
        assert generated == ["code delete"]

    def test_verify_missing_file_returns_category(self, tmp_path):
        with patch("class_generator.core.generator.render_jinja_template", return_value="class Pod:\n    pass\n"):
            _orig, generated = generate_resource_file_from_dict(
                resource_dict=self._resource_dict(),
                verify=True,
                output_dir=str(tmp_path),
            )

        assert generated == ["file does not exist"]


class TestVerifyCLI:
    """Test CLI --verify and --verify-all options."""

    def test_verify_requires_kind(self):
        result = CliRunner().invoke(cli=main, args=["--verify"])
        assert result.exit_code != 0

    def test_verify_mutually_exclusive_with_verify_all(self):
        result = CliRunner().invoke(cli=main, args=["--verify", "--verify-all", "-k", "Pod"])
        assert result.exit_code != 0

    def test_verify_mutually_exclusive_with_regenerate_all(self):
        result = CliRunner().invoke(cli=main, args=["--verify", "--regenerate-all", "-k", "Pod"])
        assert result.exit_code != 0

    def test_verify_mutually_exclusive_with_backup(self):
        result = CliRunner().invoke(cli=main, args=["--verify-all", "--backup"])
        assert result.exit_code != 0

    def test_verify_mutually_exclusive_with_overwrite(self):
        result = CliRunner().invoke(cli=main, args=["--verify", "-k", "Pod", "--overwrite"])
        assert result.exit_code != 0

    def test_verify_mutually_exclusive_with_dry_run(self):
        result = CliRunner().invoke(cli=main, args=["--verify-all", "--dry-run"])
        assert result.exit_code != 0

    def test_verify_kind_passes(self, monkeypatch):
        mock_generator = MagicMock(return_value=[])
        monkeypatch.setattr(class_generator.cli, "class_generator", mock_generator)
        # --kind verifies only files reported by discovery as generated
        monkeypatch.setattr(
            class_generator.cli,
            "discover_generated_resources",
            MagicMock(
                return_value=[
                    {"kind": "Pod", "path": "ocp_resources/pod.py", "has_user_code": False},
                    {"kind": "Service", "path": "ocp_resources/service.py", "has_user_code": False},
                ]
            ),
        )

        result = CliRunner().invoke(cli=main, args=["--verify", "-k", "Pod,Service"])

        assert result.exit_code == 0
        assert mock_generator.call_count == 2
        assert mock_generator.call_args_list[0][1]["kind"] == "Pod"
        assert mock_generator.call_args_list[1][1]["kind"] == "Service"

    def test_verify_kind_skips_hand_written_resource(self, monkeypatch, caplog):
        mock_generator = MagicMock(return_value=[])
        monkeypatch.setattr(class_generator.cli, "class_generator", mock_generator)
        # discovery never returns hand-written files, so nothing is verified for them
        monkeypatch.setattr(
            class_generator.cli,
            "discover_generated_resources",
            MagicMock(return_value=[{"kind": "Pod", "path": "ocp_resources/pod.py", "has_user_code": False}]),
        )

        result = CliRunner().invoke(cli=main, args=["--verify", "-k", "ClusterVersion"])

        assert result.exit_code == 0
        mock_generator.assert_not_called()
        assert "not generated resources" in caplog.text

    def test_verify_all_passes(self, monkeypatch, tmp_path):
        pod_file = tmp_path / "pod.py"
        monkeypatch.setattr(
            class_generator.cli,
            "discover_generated_resources",
            MagicMock(return_value=[{"kind": "Pod", "path": str(pod_file), "has_user_code": False}]),
        )
        mock_generator = MagicMock(return_value=[])
        monkeypatch.setattr(class_generator.cli, "class_generator", mock_generator)

        result = CliRunner().invoke(cli=main, args=["--verify-all"])

        assert result.exit_code == 0
        mock_generator.assert_called_once_with(
            kind="Pod",
            verify=True,
            output_file=str(pod_file),
            called_from_cli=False,
        )

    def test_verify_all_drift_fails(self, monkeypatch, tmp_path):
        pod_file = tmp_path / "pod.py"
        service_file = tmp_path / "service.py"
        monkeypatch.setattr(
            class_generator.cli,
            "discover_generated_resources",
            MagicMock(
                return_value=[
                    {"kind": "Pod", "path": str(pod_file), "has_user_code": False},
                    {"kind": "Service", "path": str(service_file), "has_user_code": False},
                ]
            ),
        )
        mock_generator = MagicMock(return_value=[(str(pod_file), ["code add"])])
        monkeypatch.setattr(class_generator.cli, "class_generator", mock_generator)

        result = CliRunner().invoke(cli=main, args=["--verify-all"])

        assert result.exit_code == 1

    def test_verify_all_with_filter(self, monkeypatch, tmp_path):
        pod_file = tmp_path / "pod.py"
        monkeypatch.setattr(
            class_generator.cli,
            "discover_generated_resources",
            MagicMock(
                return_value=[
                    {"kind": "Pod", "path": str(pod_file), "has_user_code": False},
                    {"kind": "Service", "path": str(tmp_path / "service.py"), "has_user_code": False},
                ]
            ),
        )
        mock_generator = MagicMock(return_value=[])
        monkeypatch.setattr(class_generator.cli, "class_generator", mock_generator)

        result = CliRunner().invoke(cli=main, args=["--verify-all", "--filter", "Pod*"])

        assert result.exit_code == 0
        assert mock_generator.call_count == 1
        assert mock_generator.call_args[1]["kind"] == "Pod"

    def test_verify_generator_failure_fails(self, monkeypatch, tmp_path):
        pod_file = tmp_path / "pod.py"
        monkeypatch.setattr(
            class_generator.cli,
            "discover_generated_resources",
            MagicMock(return_value=[{"kind": "Pod", "path": str(pod_file), "has_user_code": False}]),
        )
        mock_generator = MagicMock(side_effect=RuntimeError("boom"))
        monkeypatch.setattr(class_generator.cli, "class_generator", mock_generator)

        result = CliRunner().invoke(cli=main, args=["--verify-all"])

        assert result.exit_code == 1

    def test_verify_removes_stale_temp_files(self, monkeypatch, tmp_path):
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            resources_dir = tmp_path / "ocp_resources"
            resources_dir.mkdir()
            stale_file = resources_dir / f"{VERIFY_TEMP_FILE_PREFIX}_pod_abcd1234.py"
            stale_file.write_text("stale")

            monkeypatch.setattr(
                class_generator.cli,
                "discover_generated_resources",
                MagicMock(return_value=[]),
            )

            result = CliRunner().invoke(cli=main, args=["--verify-all"])

            assert result.exit_code == 0
            assert not stale_file.exists()
        finally:
            os.chdir(original_cwd)


class TestVerifyChangedCLI:
    """Test CLI --verify-changed option."""

    def test_verify_changed_mutually_exclusive_with_verify_all(self):
        result = CliRunner().invoke(cli=main, args=["--verify-changed", "--verify-all"])
        assert result.exit_code != 0

    def test_verify_changed_mutually_exclusive_with_regenerate_all(self):
        result = CliRunner().invoke(cli=main, args=["--verify-changed", "--regenerate-all"])
        assert result.exit_code != 0

    def test_verify_changed_no_generated_files_changed(self, monkeypatch):
        monkeypatch.setattr(
            class_generator.cli,
            "_changed_generated_resources",
            MagicMock(return_value=[]),
        )
        mock_generator = MagicMock(return_value=[])
        monkeypatch.setattr(class_generator.cli, "class_generator", mock_generator)

        result = CliRunner().invoke(cli=main, args=["--verify-changed"])

        assert result.exit_code == 0
        mock_generator.assert_not_called()

    def test_verify_changed_passes(self, monkeypatch, tmp_path):
        pod_file = tmp_path / "pod.py"
        monkeypatch.setattr(
            class_generator.cli,
            "_changed_generated_resources",
            MagicMock(return_value=[("Pod", str(pod_file))]),
        )
        mock_generator = MagicMock(return_value=[])
        monkeypatch.setattr(class_generator.cli, "class_generator", mock_generator)

        result = CliRunner().invoke(cli=main, args=["--verify-changed"])

        assert result.exit_code == 0
        mock_generator.assert_called_once_with(
            kind="Pod",
            verify=True,
            output_file=str(pod_file),
            called_from_cli=False,
        )

    def test_verify_changed_drift_fails(self, monkeypatch, tmp_path):
        pod_file = tmp_path / "pod.py"
        monkeypatch.setattr(
            class_generator.cli,
            "_changed_generated_resources",
            MagicMock(return_value=[("Pod", str(pod_file))]),
        )
        mock_generator = MagicMock(return_value=[(str(pod_file), ["code add"])])
        monkeypatch.setattr(class_generator.cli, "class_generator", mock_generator)

        result = CliRunner().invoke(cli=main, args=["--verify-changed"])

        assert result.exit_code == 1

    def test_verify_changed_custom_base_forwarded(self, monkeypatch, tmp_path):
        pod_file = tmp_path / "pod.py"
        mock_changed = MagicMock(return_value=[("Pod", str(pod_file))])
        monkeypatch.setattr(class_generator.cli, "_changed_generated_resources", mock_changed)
        monkeypatch.setattr(class_generator.cli, "class_generator", MagicMock(return_value=[]))

        result = CliRunner().invoke(cli=main, args=["--verify-changed", "--base", "origin/v4.21"])

        assert result.exit_code == 0
        mock_changed.assert_called_once_with(base="origin/v4.21")

    def test_changed_generated_resources_maps_git_diff(self, monkeypatch, tmp_path):
        monkeypatch.setattr(
            class_generator.cli,
            "run_command",
            MagicMock(return_value=(True, "ocp_resources/pod.py\nocp_resources/resource.py\n", "")),
        )
        monkeypatch.setattr(
            class_generator.cli,
            "discover_generated_resources",
            MagicMock(
                return_value=[
                    {"kind": "Pod", "path": "ocp_resources/pod.py", "has_user_code": False},
                    {"kind": "Service", "path": "ocp_resources/service.py", "has_user_code": False},
                ]
            ),
        )

        targets = class_generator.cli._changed_generated_resources(base="origin/main")

        assert targets == [("Pod", "ocp_resources/pod.py")]

    def test_changed_generated_resources_git_failure_exits(self, monkeypatch):
        monkeypatch.setattr(
            class_generator.cli,
            "run_command",
            MagicMock(return_value=(False, "", "unknown revision")),
        )

        result = CliRunner().invoke(cli=main, args=["--verify-changed"])

        assert result.exit_code == 1


class TestVerifyClassification:
    """Test CLI --classification and --match options."""

    def _setup_discovery(self, monkeypatch, tmp_path, drifted):
        pod_file = tmp_path / "pod.py"
        monkeypatch.setattr(
            class_generator.cli,
            "discover_generated_resources",
            MagicMock(return_value=[{"kind": "Pod", "path": str(pod_file), "has_user_code": False}]),
        )
        monkeypatch.setattr(class_generator.cli, "class_generator", MagicMock(return_value=drifted))

    def test_classification_requires_verify_mode(self):
        result = CliRunner().invoke(cli=main, args=["--classification", "blank lines"])
        assert result.exit_code != 0

    def test_classification_unknown_value_fails(self, monkeypatch, tmp_path):
        self._setup_discovery(monkeypatch, tmp_path, [])
        result = CliRunner().invoke(cli=main, args=["--verify-all", "--classification", "not-a-classification"])
        assert result.exit_code == 1

    def test_match_requires_classification(self, monkeypatch, tmp_path):
        self._setup_discovery(monkeypatch, tmp_path, [])
        result = CliRunner().invoke(cli=main, args=["--verify-all", "--match"])
        assert result.exit_code == 1

    def test_classification_match_any_includes_partial(self, monkeypatch, tmp_path):
        pod_file = str(tmp_path / "pod.py")
        # file has code drift too, but includes "blank lines" -> matches
        self._setup_discovery(monkeypatch, tmp_path, [(pod_file, ["blank lines", "code add"])])
        result = CliRunner().invoke(cli=main, args=["--verify-all", "--classification", "blank lines"])
        assert result.exit_code == 1
        assert "class-generator --kind Pod --overwrite" in result.output
        assert "Or regenerate all drifted kinds at once:" in result.output

    def test_classification_match_flag_excludes_partial(self, monkeypatch, tmp_path):
        pod_file = str(tmp_path / "pod.py")
        # file has more than "blank lines" -> exact match excludes it
        self._setup_discovery(monkeypatch, tmp_path, [(pod_file, ["blank lines", "code add"])])
        result = CliRunner().invoke(cli=main, args=["--verify-all", "--classification", "blank lines", "--match"])
        assert result.exit_code == 0

    def test_classification_match_flag_includes_exact(self, monkeypatch, tmp_path):
        pod_file = str(tmp_path / "pod.py")
        self._setup_discovery(monkeypatch, tmp_path, [(pod_file, ["blank lines"])])
        result = CliRunner().invoke(cli=main, args=["--verify-all", "--classification", "blank lines", "--match"])
        assert result.exit_code == 1

    def test_classification_match_flag_multiple_values(self, monkeypatch, tmp_path):
        pod_file = str(tmp_path / "pod.py")
        # exactly the two given classifications -> exact match
        self._setup_discovery(monkeypatch, tmp_path, [(pod_file, ["blank lines", "code add"])])
        result = CliRunner().invoke(
            cli=main, args=["--verify-all", "--classification", "blank lines,code add", "--match"]
        )
        assert result.exit_code == 1

    def test_classification_match_flag_includes_subset(self, monkeypatch, tmp_path):
        pod_file = str(tmp_path / "pod.py")
        # only one of the two given classifications: within the requested set -> --match includes it
        self._setup_discovery(monkeypatch, tmp_path, [(pod_file, ["blank lines"])])
        result = CliRunner().invoke(
            cli=main, args=["--verify-all", "--classification", "blank lines,code add", "--match"]
        )
        assert result.exit_code == 1

    def test_match_reports_files_within_classifications_only(self, monkeypatch, tmp_path):
        # r4/r5 carry classifications outside the requested set -> excluded by --match
        drifted = [
            ("r1.py", ["docstring add"]),
            ("r2.py", ["docstring delete"]),
            ("r3.py", ["docstring add", "docstring delete"]),
            ("r4.py", ["docstring add", "docstring delete", "code add"]),
            ("r5.py", ["docstring add", "code remove"]),
        ]
        self._setup_discovery(monkeypatch, tmp_path, drifted)
        result = CliRunner().invoke(
            cli=main, args=["--verify-all", "--classification", "docstring add,docstring delete", "--match"]
        )
        assert result.exit_code == 1
        for reported in ("r1.py", "r2.py", "r3.py"):
            assert reported in result.output
        for excluded in ("r4.py", "r5.py"):
            assert excluded not in result.output
        assert "2 drifted file(s) did not match" in result.output

    def test_exclude_requires_verify_mode(self):
        result = CliRunner().invoke(cli=main, args=["--exclude", "breaking change"])
        assert result.exit_code != 0

    def test_exclude_unknown_value_fails(self, monkeypatch, tmp_path):
        self._setup_discovery(monkeypatch, tmp_path, [])
        result = CliRunner().invoke(cli=main, args=["--verify-all", "--exclude", "not-a-classification"])
        assert result.exit_code == 1

    def test_exclude_drops_breaking_files(self, monkeypatch, tmp_path):
        # only breaking drift present -> everything excluded -> run passes and shows nothing
        self._setup_discovery(
            monkeypatch,
            tmp_path,
            [("safe.py", ["blank lines"]), ("risky.py", ["breaking change", "code delete"])],
        )
        result = CliRunner().invoke(cli=main, args=["--verify-all", "--exclude", "breaking change"])
        assert result.exit_code == 1
        assert "safe.py" in result.output
        assert "risky.py" not in result.output
        assert "1 drifted file(s) excluded by --exclude 'breaking change'" in result.output

    def test_exclude_all_files_passes(self, monkeypatch, tmp_path):
        self._setup_discovery(monkeypatch, tmp_path, [("risky.py", ["breaking change", "code delete"])])
        result = CliRunner().invoke(cli=main, args=["--verify-all", "--exclude", "breaking change"])
        assert result.exit_code == 0
        assert "Verification passed" in result.output

    def test_exclude_multiple_values(self, monkeypatch, tmp_path):
        self._setup_discovery(
            monkeypatch,
            tmp_path,
            [
                ("a.py", ["breaking change"]),
                ("b.py", ["schema incomplete"]),
                ("c.py", ["blank lines"]),
            ],
        )
        result = CliRunner().invoke(cli=main, args=["--verify-all", "--exclude", "breaking change,schema incomplete"])
        assert result.exit_code == 1
        assert "c.py" in result.output
        assert "a.py" not in result.output
        assert "b.py" not in result.output

    def test_classification_no_match_passes(self, monkeypatch, tmp_path):
        pod_file = str(tmp_path / "pod.py")
        self._setup_discovery(monkeypatch, tmp_path, [(pod_file, ["code delete"])])
        result = CliRunner().invoke(cli=main, args=["--verify-all", "--classification", "blank lines"])
        assert result.exit_code == 0


class TestVerifyNotInSchema:
    """Test classification of kinds absent from the resources mapping."""

    def test_not_in_schema_kind_reported_with_category(self, monkeypatch, tmp_path):
        pod_file = str(tmp_path / "pod.py")
        monkeypatch.setattr(
            class_generator.cli,
            "discover_generated_resources",
            MagicMock(return_value=[{"kind": "Pod", "path": pod_file, "has_user_code": False}]),
        )
        monkeypatch.setattr(class_generator.cli, "read_resources_mapping_file", MagicMock(return_value={}))
        result = CliRunner().invoke(cli=main, args=["--verify-all"])
        assert result.exit_code == 1
        assert "(not in schema)" in result.output

    def test_not_in_schema_filtered_by_classification(self, monkeypatch, tmp_path):
        pod_file = str(tmp_path / "pod.py")
        monkeypatch.setattr(
            class_generator.cli,
            "discover_generated_resources",
            MagicMock(return_value=[{"kind": "Pod", "path": pod_file, "has_user_code": False}]),
        )
        monkeypatch.setattr(class_generator.cli, "read_resources_mapping_file", MagicMock(return_value={}))
        result = CliRunner().invoke(cli=main, args=["--verify-all", "--classification", "blank lines"])
        assert result.exit_code == 0

    def test_not_in_schema_kind_excluded_from_regen_commands(self, monkeypatch, tmp_path):
        pod_file = str(tmp_path / "pod.py")
        monkeypatch.setattr(
            class_generator.cli,
            "discover_generated_resources",
            MagicMock(return_value=[{"kind": "Pod", "path": pod_file, "has_user_code": False}]),
        )
        monkeypatch.setattr(class_generator.cli, "read_resources_mapping_file", MagicMock(return_value={}))
        result = CliRunner().invoke(cli=main, args=["--verify-all"])
        assert result.exit_code == 1
        assert "class-generator --kind Pod --overwrite" not in result.output
        assert "Run --update-schema from a cluster that serves these kinds" in result.output

    def test_format_file_converges_on_raw_render(self):
        """A raw (unformatted) render must converge to a stable fixpoint via _format_file."""
        raw = (
            '"""Doc."""\n'
            "from typing import Any\n"
            "\n"
            "\n"
            "class Foo:\n"
            "    def bar(self) -> None:\n"
            "\n"
            "        x:Any=1\n"
            "        print(x)\n"
        )
        # prek needs repository context: the file must live inside the repo
        target = Path("ocp_resources") / f"{VERIFY_TEMP_FILE_PREFIX}_test_converge.py"
        try:
            target.write_text(raw, encoding="utf-8")
            _format_file(filepath=str(target))
            assert "x: Any = 1" in target.read_text(encoding="utf-8")
        finally:
            target.unlink(missing_ok=True)


class TestVerifyMultiGroupKind:
    """A kind that renders one file per API group must compare each variant to its own file."""

    def test_verify_ignores_pinned_output_file(self, tmp_path, monkeypatch):
        compared: list[str] = []

        def fake_verify_rendered(filepath: str, output: str) -> list[str] | None:
            compared.append(filepath)
            return None

        monkeypatch.setattr("class_generator.core.generator.verify_rendered", fake_verify_rendered)

        base_kwargs: dict[str, Any] = {
            "kind": "Config",
            "base_class": "Resource",
            "api_version": "v1",
            "version": "v1",
            "description": "Config is a test resource.",
            "namespaced": False,
            "fields": [],
            "spec": [],
        }

        # two variants of the same kind, each with its own API group
        for group, suffix in (
            ("config.openshift.io", ""),
            ("samples.operator.openshift.io", "samples_operator_openshift_io"),
        ):
            generate_resource_file_from_dict(
                resource_dict={**base_kwargs, "group": group, "api_group": group},
                output_file=str(tmp_path / "pinned_wrong_path.py"),
                output_file_suffix=suffix,
                output_dir=str(tmp_path),
                verify=True,
            )

        # each variant is compared against the file regeneration would write for it
        assert compared == [
            str(tmp_path / "config.py"),
            str(tmp_path / "config_samples_operator_openshift_io.py"),
        ]


class TestRequiredParameterDrift:
    """A parameter that becomes required breaks callers that omit it."""

    def test_optional_to_required_is_breaking(self):
        committed = (
            "class A:\n    def __init__(self, a=None):\n        self.a = a\n    def to_dict(self):\n        pass\n"
        )
        rendered = (
            "class A:\n"
            "    def __init__(self, a=None):\n"
            "        self.a = a\n"
            "    def to_dict(self):\n"
            "        if self.a is None:\n"
            '            raise MissingRequiredArgumentError(argument="self.a")\n'
        )
        assert "breaking change" in classify_drift(committed=committed, rendered=rendered)

    def test_required_to_optional_is_not_breaking(self):
        committed = (
            "class A:\n"
            "    def __init__(self, a=None):\n"
            "        self.a = a\n"
            "    def to_dict(self):\n"
            "        if self.a is None:\n"
            '            raise MissingRequiredArgumentError(argument="self.a")\n'
        )
        rendered = (
            "class A:\n    def __init__(self, a=None):\n        self.a = a\n    def to_dict(self):\n        pass\n"
        )
        assert "breaking change" not in classify_drift(committed=committed, rendered=rendered)


class TestCallerVisibleBreakingChanges:
    """Every change that makes previously working caller code fail or behave differently."""

    BASE = (
        "class A(Resource):\n"
        '    api_group: str = "g.io"\n'
        '    api_version: str = "v1"\n'
        "    def __init__(self, a=None):\n"
        "        self.a = a\n"
        "    def to_dict(self):\n"
        '        self.res["a"] = self.a\n'
    )

    def test_base_class_change_is_breaking(self):
        rendered = self.BASE.replace("class A(Resource)", "class A(NamespacedResource)")
        assert "breaking change" in classify_drift(committed=self.BASE, rendered=rendered)

    def test_api_group_change_is_breaking(self):
        rendered = self.BASE.replace('"g.io"', '"other.io"')
        assert "breaking change" in classify_drift(committed=self.BASE, rendered=rendered)

    def test_api_version_change_is_breaking(self):
        rendered = self.BASE.replace('"v1"', '"v1beta1"')
        assert "breaking change" in classify_drift(committed=self.BASE, rendered=rendered)

    def test_emitted_api_key_change_is_breaking(self):
        rendered = self.BASE.replace('self.res["a"]', 'self.res["b"]')
        assert "breaking change" in classify_drift(committed=self.BASE, rendered=rendered)

    def test_unchanged_resource_is_not_breaking(self):
        assert classify_drift(committed=self.BASE, rendered=self.BASE) == []
