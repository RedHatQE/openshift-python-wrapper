"""File writing utilities for generated code."""

import ast
import contextlib
import difflib
import threading
import uuid
from pathlib import Path

from pyhelper_utils.shell import run_command
from simple_logger.logger import get_logger

LOGGER = get_logger(name=__name__)

# Project root directory (contains pyproject.toml and .pre-commit-config.yaml)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# prek hooks are not safe under concurrent invocation (mypy cache, git stash
# contention), and file writes must not land inside a prek run's stash window;
# write + prek runs are serialized atomically within this process
_PREK_LOCK = threading.RLock()


def _run_prek(command: list[str], locked: bool = True) -> tuple[bool, str, str]:
    """Run a prek command, by default under the process-wide prek lock."""
    lock_context = _PREK_LOCK if locked else contextlib.nullcontext()
    with lock_context:
        rc, stdout, stderr = run_command(
            command=command,
            verify_stderr=False,
            check=False,
            log_errors=False,
        )
    return rc, stdout, stderr


def _format_file(filepath: str, locked: bool = True) -> None:
    """
    Format a file with prek — the project's pre-commit hooks, unmodified settings.

    If the first prek run exits non-zero (a hook failed or modified the file),
    prek runs again — the second run must pass clean. No other formatter is ever
    invoked, so a file that passes here also passes CI.

    Args:
        filepath: Path to the file to format
        locked: Hold the process-wide prek lock. Required for tracked files written
            by parallel generation workers (a write landing inside prek's stash
            window corrupts the run). Verify temp files are untracked and nothing
            writes tracked files during verification, so they run lock-free and
            prek invocations proceed in parallel.
    """
    pre_commit_config = str(_PROJECT_ROOT / ".pre-commit-config.yaml")
    command = ["uvx", "prek", "-c", pre_commit_config, "run", "--files", filepath]
    try:
        rc, stdout, stderr = _run_prek(command=command, locked=locked)
    except Exception as e:
        raise RuntimeError(f"Failed to run prek for {filepath}: {e}") from e

    if rc:
        return

    if stdout:
        LOGGER.debug(f"{filepath} processed by prek")

    rc, stdout, stderr = _run_prek(command=command, locked=locked)
    if not rc:
        raise RuntimeError(
            f"prek hooks failed twice for {filepath}: stdout: {stdout.strip()[:400]} stderr: {stderr.strip()[:200]}"
        )


def write_and_format_rendered(filepath: str, output: str) -> None:
    """
    Write rendered content to file and format with prek, atomically.

    The write and the prek run share one lock: a file written by another worker
    during a prek run lands inside prek's stash window and corrupts the run.

    Args:
        filepath: Path to write the file to
        output: Content to write
    """
    with _PREK_LOCK:
        Path(filepath).write_text(output, encoding="utf-8")
        _format_file(filepath=filepath)


DRIFT_CATEGORIES = (
    "blank lines",
    "docstring add",
    "docstring delete",
    "code add",
    "code delete",
    "signature code add",
    "signature code remove",
    "breaking change",
    "schema incomplete",
    "file does not exist",
    "formatting failed",
    "not in schema",
)

DRIFT_CATEGORY_DESCRIPTIONS = {
    "blank lines": "only blank-line differences (formatting drift)",
    "docstring add": "generator output adds docstring text the file lacks",
    "docstring delete": "generator output removes docstring text the file has",
    "code add": "generator output adds code lines the file lacks",
    "code delete": "generator output removes code lines the file has",
    "signature code add": "__init__ parameters added (all generated params have defaults - non-breaking)",
    "signature code remove": "__init__ parameters removed from the generated signature",
    "breaking change": "a parameter was removed - callers passing it now get TypeError",
    "schema incomplete": "rendered class has no parameters while the file has some (unresolvable schema $ref)",
    "file does not exist": "expected generated file is missing",
    "formatting failed": "rendered output could not be formatted",
    "not in schema": "kind is absent from the resources mapping",
}


def _docstring_spans(source: str) -> list[tuple[int, int]]:
    """
    Return the (start, end) line ranges of all docstrings in the source.

    Args:
        source: Python source code

    Returns:
        List of (start_line, end_line) tuples, 1-based, inclusive
    """
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []
    spans: list[tuple[int, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            body = node.body
            if (
                body
                and isinstance(body[0], ast.Expr)
                and isinstance(body[0].value, ast.Constant)
                and isinstance(body[0].value.value, str)
            ):
                end_lineno = body[0].end_lineno
                if end_lineno is not None:
                    spans.append((body[0].lineno, end_lineno))
    return spans


def classify_drift(committed: str, rendered: str) -> list[str]:
    """
    Classify the differences between committed content and class-generator rendered output.

    Categories:
    - "blank lines": whitespace-only diff lines
    - "docstring delete": docstring lines regeneration would remove (committed has extra)
    - "docstring add": docstring lines regeneration would introduce
    - "code delete": code lines regeneration would remove (committed has extra)
    - "code add": code lines regeneration would introduce
    - "signature code add": __init__ parameters added (non-breaking)
    - "signature code remove": __init__ parameters removed
    - "breaking change": a parameter was removed (breaking for callers)
    - "schema incomplete": rendered class lost all parameters (unresolvable schema ref)

    Args:
        committed: Content of the committed file
        rendered: Content rendered by the generator

    Returns:
        Sorted list of drift categories; empty when contents are identical
    """
    flags: set[str] = set()
    old_spans = _docstring_spans(committed)
    new_spans = _docstring_spans(rendered)

    def line_kind(line_no: int, spans: list[tuple[int, int]], text: str) -> str:
        if not text.strip():
            return "blank"
        if any(start <= line_no <= end for start, end in spans):
            return "docstring"
        return "code"

    old_lineno = new_lineno = 0
    for line in difflib.unified_diff(
        committed.splitlines(keepends=True),
        rendered.splitlines(keepends=True),
        n=0,
    ):
        if line.startswith("@@"):
            parts = line.split()
            old_lineno = int(parts[1].lstrip("-").split(",")[0])
            new_lineno = int(parts[2].lstrip("+").split(",")[0])
            continue
        if line.startswith("---") or line.startswith("+++"):
            continue
        if line.startswith("-"):
            kind = line_kind(old_lineno, old_spans, line[1:])
            flags.add({"blank": "blank lines", "docstring": "docstring delete", "code": "code delete"}[kind])
            old_lineno += 1
        elif line.startswith("+"):
            kind = line_kind(new_lineno, new_spans, line[1:])
            flags.add({"blank": "blank lines", "docstring": "docstring add", "code": "code add"}[kind])
            new_lineno += 1
        else:
            old_lineno += 1
            new_lineno += 1

    def init_params(source: str) -> list[str]:
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "__init__":
                return [arg.arg for arg in node.args.args if arg.arg != "self"]
        return []

    old_params = set(init_params(committed))
    new_params = set(init_params(rendered))
    if new_params - old_params:
        # Generated params always carry defaults ("| None = None"), so an added param
        # cannot break callers
        flags.add("signature code add")
    if old_params - new_params:
        flags.add("signature code remove")
        # A removed param breaks callers: the kwarg flows through **kwargs into
        # Resource.__init__, which has a fixed parameter list -> TypeError
        flags.add("breaking change")
    if old_params and not new_params:
        # Every parameter vanished: the rendered class is effectively empty, so the
        # schema $ref could not be resolved - the wall of removals above is a schema
        # gap, not an API change
        flags.add("schema incomplete")

    return sorted(flags)


def verify_rendered(filepath: str, output: str) -> list[str] | None:
    """
    Verify that rendered content matches an existing file without modifying it.

    Renders the output to a temporary file (created next to the target file so
    prek hooks run with the same repository context), applies the same
    formatting as `write_and_format_rendered`, and compares the results.
    On mismatch, logs a unified diff of the differences.

    Args:
        filepath: Path to the existing file to verify against
        output: Rendered content to verify

    Returns:
        None if the formatted rendered output is identical to the existing file,
        otherwise the list of drift categories (see `classify_drift`)
    """
    target_file = Path(filepath)
    if not target_file.exists():
        LOGGER.error(f"Verify failed: {filepath} does not exist")
        return ["file does not exist"]

    # Temporary file in the same directory keeps prek hooks operating with the
    # repository context. It is NOT gitignored (prek/ruff skips gitignored
    # files); it is always removed, even on failure, and stale files from
    # interrupted runs are cleaned up at the start of every verify run.
    tmp_file = target_file.parent / f".class_generator_verify_{target_file.stem}_{uuid.uuid4().hex[:8]}.py"
    format_failed = False
    try:
        # Untracked temp file: prek runs lock-free so verification stays parallel
        # (concurrent prek on untracked files is safe; only tracked writes need
        # the lock)
        tmp_file.write_text(output, encoding="utf-8")
        _format_file(filepath=str(tmp_file), locked=False)
        rendered_content = tmp_file.read_text(encoding="utf-8")
    except Exception as e:
        LOGGER.error(f"Verify failed: could not format rendered output for {filepath}: {e}")
        format_failed = True
        # Fall back to the unformatted rendered output so the drift report
        # (classification + diff) is still produced
        rendered_content = output
    finally:
        tmp_file.unlink(missing_ok=True)

    committed_content = target_file.read_text(encoding="utf-8")
    if rendered_content == committed_content and not format_failed:
        return None

    if format_failed and rendered_content == committed_content:
        LOGGER.error(f"Verify failed for {filepath}: rendered output could not be formatted for comparison")
        return ["formatting failed"]

    diff = "".join(
        difflib.unified_diff(
            committed_content.splitlines(keepends=True),
            rendered_content.splitlines(keepends=True),
            fromfile=f"{filepath} (committed)",
            tofile=f"{filepath} (class-generator output)",
        )
    )
    categories = classify_drift(committed=committed_content, rendered=rendered_content)
    LOGGER.error(
        f"Drift detected in {filepath} - categories: {', '.join(categories)}\n"
        f"diff (committed vs class-generator output):\n{diff}"
    )
    return categories
