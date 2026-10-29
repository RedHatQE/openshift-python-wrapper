"""Tests for the custom VirtualMachineFileRestore helpers."""

from collections.abc import Callable
from typing import Any
from unittest.mock import PropertyMock, patch

import pytest

from fake_kubernetes_client.dynamic_client import FakeDynamicClient
from ocp_resources.virtual_machine_file_restore import VirtualMachineFileRestore


@pytest.fixture()
def vmfr_client(fake_client: FakeDynamicClient) -> FakeDynamicClient:
    fake_client.register_resources(
        resources={
            "kind": "VirtualMachineFileRestore",
            "api_version": "v1alpha1",
            "group": "filerestore.kubevirt.io",
            "namespaced": True,
            "plural": "virtualmachinefilerestores",
        }
    )
    return fake_client


@pytest.mark.parametrize(
    ("factory", "source_name_argument", "source_kind"),
    [
        (VirtualMachineFileRestore.from_snapshot, "source_snapshot_name", "snapshot"),
        (VirtualMachineFileRestore.from_pvc, "source_pvc_name", "pvc"),
    ],
)
@pytest.mark.parametrize("source_namespace", [None, "backup-ns"])
@pytest.mark.parametrize("source_path", [None, "/etc/config"])
def test_factory_builds_source_and_target(
    vmfr_client: FakeDynamicClient,
    factory: Callable[..., VirtualMachineFileRestore],
    source_name_argument: str,
    source_kind: str,
    source_namespace: str | None,
    source_path: str | None,
) -> None:
    restore = factory(
        target_vm_name="target-vm",
        **{source_name_argument: "backup-volume"},
        source_namespace=source_namespace,
        source_path=source_path,
        client=vmfr_client,
        name="test-restore",
        namespace="target-ns",
        teardown=False,
    )

    expected_source = {"name": "backup-volume"}
    if source_namespace is not None:
        expected_source["namespace"] = source_namespace

    assert restore.source == {source_kind: expected_source}
    assert restore.target == {"apiGroup": "kubevirt.io", "kind": "VirtualMachine", "name": "target-vm"}
    assert restore.source_path == source_path
    assert restore.client is vmfr_client
    assert restore.name == "test-restore"
    assert restore.namespace == "target-ns"
    assert restore.teardown is False


@pytest.mark.parametrize(
    ("instance", "expected_count"),
    [
        ({}, None),
        ({"status": {}}, None),
        ({"status": {"restoredFilesCount": 0}}, 0),
        ({"status": {"restoredFilesCount": 3}}, 3),
    ],
)
def test_restored_files_count(
    vmfr_client: FakeDynamicClient, instance: dict[str, Any], expected_count: int | None
) -> None:
    restore = VirtualMachineFileRestore(client=vmfr_client, name="test-restore", namespace="target-ns")
    with patch.object(VirtualMachineFileRestore, "instance", new_callable=PropertyMock, return_value=instance):
        assert restore.restored_files_count == expected_count
