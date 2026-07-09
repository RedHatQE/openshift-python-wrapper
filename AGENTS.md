# openshift-python-wrapper

Python wrapper for kubernetes-python-client providing simplified CRUD and resource-specific methods for Kubernetes/OpenShift resources (233+ wrappers).

## Commands

- **Package manager**: `uv` — NEVER use `python` or `pip` directly
- Build/sync: `uv sync`
- Test all: `uv run --group tests pytest`
- Test specific: `uv run --group tests pytest tests/test_daemonset.py`
- Lint: `prek run`
- Pre-commit setup: `prek install`
- Generate resource: `class-generator --kind Pod --add-tests`
- Full verify: `prek run && uv run --group tests pytest`

## Definition of Done

A task is complete when ALL pass:
1. `prek run` exits 0 (ruff, mypy, flake8, detect-secrets, gitleaks)
2. `uv run --group tests pytest` exits 0 — coverage ≥ 65%
3. Type hints on all new code (enforced by mypy)
4. Committed with message: `type(scope): description`

## When Blocked

- Tests fail after 3 attempts → stop, report failing test with full output
- Missing dependency → `uv add <package>`, never `pip install`
- Pre-commit fails → read the error, fix the specific violation
- 🚫 NEVER: skip tests, force push to main, delete files to fix errors

## Project

- Stack: Python 3.10+, kubernetes-python-client, timeout-sampler, uv
- Structure: `ocp_resources/` (resource wrappers), `tests/` (pytest), `class_generator/` (code gen), `fake_kubernetes_client/` (mock client)
- Key deps: `kubernetes` (API client), `timeout-sampler` (polling), `openshift-python-utilities` (shared utils)
- Docs: `examples/`, inline docstrings (Google style)

## When Adding a Resource

- New resources MUST be generated via `class-generator --kind ResourceName --add-tests` — manual creation is not allowed
- Reference implementations: `ocp_resources/config_map.py` (namespaced), `ocp_resources/node.py` (cluster-scoped)
- File naming: `snake_case.py` — class naming: exact Kubernetes `kind` (PascalCase)
- Namespaced → inherit `NamespacedResource`, cluster-scoped → inherit `Resource`
- Must implement: `__init__()`, `to_dict()`, `api_group` (if not core v1)
- Reference: `class_generator/README.md`

## Generated Code Markers

Resource files from `class-generator` use markers to separate generated from manual code:
- **Start**: `# Generated using https://...class_generator/README.md` (line 1)
- **End**: `# End of generated code` (inside class)

Code between markers is auto-generated — do NOT modify manually. Use `class-generator --kind <Kind> --overwrite --backup` to regenerate. Custom code (helper methods, overrides) goes BELOW the end marker.

## When Writing Code

- No client-side validation in `to_dict()` — let the K8s/OCP API server return errors. Helper functions in resource classes CAN validate.
- Context managers for auto-cleanup: `with Pod(name="test", namespace="default") as pod:`
- Wait utilities: `wait_for_status()`, `wait_for_condition()` via timeout-sampler
- Sensitive data: add keys to `keys_to_hash` property for automatic log hashing
- Fake client for tests: `get_client(fake=True)` — no cluster required

## When Reviewing Code

- Verify generated code markers are intact — no manual edits between markers
- Check type hints on all new functions/parameters
- Verify tests exist for new helper methods (not needed for generated `__init__`/`to_dict`)
- Import path: `ocp_resources.resource_name` (snake_case with underscores)

## Boundaries

- ✅ Always: use `uv` for Python ops, run `prek install` before first commit, add typing
- ⚠️ Ask first: adding new dependencies, modifying base `Resource` class, changing CI
- 🚫 Never: use `python`/`pip` directly, edit generated code between markers, edit files in `docs/` (regenerate with docsfy instead)

## Environment

```bash
OPENSHIFT_PYTHON_WRAPPER_LOG_LEVEL=DEBUG        # DEBUG, INFO, WARNING, ERROR, CRITICAL
OPENSHIFT_PYTHON_WRAPPER_HASH_LOG_DATA="false"   # Disable log hashing
HTTPS_PROXY="http://proxy:8080"                  # Proxy support
```

## Additional References

- Contributing guide: `CONTRIBUTING.md`
- Class generator details: `class_generator/README.md`
- MCP server: `mcp_server/README.md`
- Release process: `CONTRIBUTING.md` + `.release-it.json`
- Fake client: `fake_kubernetes_client/` (CRUD, selectors, watch, status generation)
