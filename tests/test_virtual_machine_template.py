from typing import Any
from unittest.mock import MagicMock

import pytest

from ocp_resources.resource import get_client
from ocp_resources.virtual_machine_template import VirtualMachineTemplate

# ── constants ────────────────────────────────────────────────────────────────

VMT_NAMESPACE = "test-ns"
VMT_NAME = "test-vmt"
_API_GROUP = "template.kubevirt.io"
_API_VERSION = "v1alpha1"
_FULL_API_VERSION = f"{_API_GROUP}/{_API_VERSION}"
# The process method builds: "subresources.<self.api_version>"
_SUBRESOURCES_API = f"subresources.{_FULL_API_VERSION}"
# Expected POST path used by process()
VMT_PROCESS_PATH = f"/apis/{_SUBRESOURCES_API}/namespaces/{VMT_NAMESPACE}/virtualmachinetemplates/{VMT_NAME}/process"

# Resource definition required to register VirtualMachineTemplate in the fake client
_VMT_RESOURCE_DEF: dict[str, Any] = {
    "kind": "VirtualMachineTemplate",
    "api_version": _API_VERSION,
    "group": _API_GROUP,
    "version": _API_VERSION,
    "group_version": _FULL_API_VERSION,
    "plural": "virtualmachinetemplates",
    "singular": "virtualmachinetemplate",
    "namespaced": True,
}


# ── helpers ───────────────────────────────────────────────────────────────────


def _make_fake_client(response_data: dict[str, Any] | None = None) -> Any:
    """
    Return a fake client (get_client(fake=True)) with VirtualMachineTemplate registered
    and request() replaced by a MagicMock so call args and return values are inspectable.
    """
    client = get_client(fake=True)
    client.register_resources(_VMT_RESOURCE_DEF)
    mock_response = MagicMock()
    mock_response.to_dict.return_value = response_data if response_data is not None else {}
    # Intentionally replacing the stub method with a MagicMock for call-arg inspection
    client.request = MagicMock(return_value=mock_response)  # type: ignore[method-assign]
    return client


# ── fixtures ──────────────────────────────────────────────────────────────────


@pytest.fixture()
def vmt() -> VirtualMachineTemplate:
    return VirtualMachineTemplate(
        client=_make_fake_client(),
        name=VMT_NAME,
        namespace=VMT_NAMESPACE,
        virtual_machine={"spec": {}},
    )


# ── tests ─────────────────────────────────────────────────────────────────────


class TestProcessPath:
    """process() sends a POST to the correct subresource URL."""

    def test_process_default_parameters_uses_correct_path(self, vmt: VirtualMachineTemplate) -> None:
        process_client = _make_fake_client()
        vmt.process(client=process_client)

        method, path, _ = process_client.request.call_args.args
        assert method == "POST"
        assert path == VMT_PROCESS_PATH

    def test_process_with_parameters_uses_correct_path(self, vmt: VirtualMachineTemplate) -> None:
        process_client = _make_fake_client()
        vmt.process(parameters={"NAME": "my-vm"}, client=process_client)

        method, path, _ = process_client.request.call_args.args
        assert method == "POST"
        assert path == VMT_PROCESS_PATH


class TestProcessOptionsBody:
    """process() sends the correct ProcessOptions body."""

    def test_body_kind_is_process_options(self, vmt: VirtualMachineTemplate) -> None:
        process_client = _make_fake_client()
        vmt.process(client=process_client)

        _, _, body = process_client.request.call_args.args
        assert body["kind"] == "ProcessOptions"

    def test_body_api_version_matches_subresources_api(self, vmt: VirtualMachineTemplate) -> None:
        process_client = _make_fake_client()
        vmt.process(client=process_client)

        _, _, body = process_client.request.call_args.args
        assert body["apiVersion"] == _SUBRESOURCES_API

    def test_body_parameters_empty_when_none_supplied(self, vmt: VirtualMachineTemplate) -> None:
        """parameters=None should produce an empty dict in the request body."""
        process_client = _make_fake_client()
        vmt.process(client=process_client)

        _, _, body = process_client.request.call_args.args
        assert body["parameters"] == {}

    def test_body_parameters_passed_through_when_supplied(self, vmt: VirtualMachineTemplate) -> None:
        """Supplied parameters dict should appear unchanged in the request body."""
        supplied = {"NAME": "my-vm", "INSTANCETYPE": "u1.large"}
        process_client = _make_fake_client()
        vmt.process(parameters=supplied, client=process_client)

        _, _, body = process_client.request.call_args.args
        assert body["parameters"] == supplied


class TestProcessClientSelection:
    """process() uses the injected client, falling back to self.client."""

    def test_process_uses_injected_client(self, vmt: VirtualMachineTemplate) -> None:
        injected = _make_fake_client()
        vmt.process(client=injected)

        injected.request.assert_called_once()
        vmt.client.request.assert_not_called()

    def test_process_falls_back_to_self_client_when_not_injected(self, vmt: VirtualMachineTemplate) -> None:
        vmt.client.request.return_value.to_dict.return_value = {}
        vmt.process()

        vmt.client.request.assert_called_once()


class TestProcessReturnValue:
    """process() returns the raw response object from the API client."""

    def test_process_returns_raw_response(self, vmt: VirtualMachineTemplate) -> None:
        process_client = _make_fake_client()

        result = vmt.process(client=process_client)

        assert result is process_client.request.return_value
