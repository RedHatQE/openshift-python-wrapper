from collections.abc import Callable
from typing import Any
from unittest.mock import PropertyMock, patch

import pytest
from timeout_sampler import TimeoutExpiredError

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
@pytest.mark.parametrize("source_namespace", [None, "backup-ns", ""])
@pytest.mark.parametrize("source_path", [None, "/etc/config", ""])
def test_factory_builds_restore_manifest(
    vmfr_client: FakeDynamicClient,
    factory: Callable[..., VirtualMachineFileRestore],
    source_name_argument: str,
    source_kind: str,
    source_namespace: str | None,
    source_path: str | None,
) -> None:
    """Factories preserve source options and forward resource arguments to the constructor."""
    restore = factory(
        target_vm_name="target-vm",
        **{source_name_argument: "backup-volume"},
        source_namespace=source_namespace,
        source_path=source_path,
        client=vmfr_client,
        name="test-restore",
        namespace="target-ns",
        label={"purpose": "file-restore"},
        teardown=False,
    )
    restore.to_dict()

    expected_source = {"name": "backup-volume"}
    if source_namespace is not None:
        expected_source["namespace"] = source_namespace
    expected_spec: dict[str, Any] = {
        "source": {source_kind: expected_source},
        "target": {"apiGroup": "kubevirt.io", "kind": "VirtualMachine", "name": "target-vm"},
    }
    if source_path is not None:
        expected_spec["sourcePath"] = source_path

    assert restore.res == {
        "apiVersion": "filerestore.kubevirt.io/v1alpha1",
        "kind": "VirtualMachineFileRestore",
        "metadata": {
            "name": "test-restore",
            "namespace": "target-ns",
            "labels": {"purpose": "file-restore"},
        },
        "spec": expected_spec,
    }
    assert restore.client is vmfr_client
    assert restore.teardown is False
    assert not restore.exists


@pytest.fixture()
def vmfr(vmfr_client: FakeDynamicClient) -> VirtualMachineFileRestore:
    return VirtualMachineFileRestore.from_snapshot(
        target_vm_name="target-vm",
        source_snapshot_name="backup-snapshot",
        client=vmfr_client,
        name="test-restore",
        namespace="target-ns",
    )


@pytest.mark.parametrize(
    "target_phase",
    [VirtualMachineFileRestore.Phase.SUCCEEDED, VirtualMachineFileRestore.Phase.VOLUME_READY],
)
def test_wait_for_phase_waits_through_intermediate_phases(vmfr: VirtualMachineFileRestore, target_phase: str) -> None:
    with patch.object(
        VirtualMachineFileRestore,
        "instance",
        new_callable=PropertyMock,
        side_effect=[{}, {"status": {"phase": "Init"}}, {"status": {"phase": target_phase}}],
    ) as instance:
        vmfr.wait_for_phase(target_phase=target_phase, timeout=1, sleep=0)
        assert instance.call_count == 3


def test_wait_for_phase_reports_failure_details(vmfr: VirtualMachineFileRestore) -> None:
    with patch.object(
        VirtualMachineFileRestore,
        "instance",
        new_callable=PropertyMock,
        return_value={"status": {"phase": "Failed", "errorMessage": "Backup snapshot is missing"}},
    ):
        with pytest.raises(RuntimeError, match="test-restore.*Backup snapshot is missing"):
            vmfr.wait_for_phase(target_phase=vmfr.Phase.SUCCEEDED, timeout=1, sleep=0)


def test_wait_for_phase_allows_expected_failure(vmfr: VirtualMachineFileRestore) -> None:
    with patch.object(
        VirtualMachineFileRestore,
        "instance",
        new_callable=PropertyMock,
        return_value={"status": {"phase": "Failed"}},
    ):
        vmfr.wait_for_phase(target_phase=vmfr.Phase.FAILED, timeout=1, sleep=0)


def test_wait_for_phase_times_out(vmfr: VirtualMachineFileRestore) -> None:
    with patch.object(
        VirtualMachineFileRestore,
        "instance",
        new_callable=PropertyMock,
        return_value={"status": {"phase": "Restoring"}},
    ):
        with pytest.raises(TimeoutExpiredError):
            vmfr.wait_for_phase(target_phase=vmfr.Phase.SUCCEEDED, timeout=0, sleep=0)


@pytest.mark.parametrize(
    ("instance", "expected_count"),
    [
        ({}, None),
        ({"status": {}}, None),
        ({"status": {"restoredFilesCount": 0}}, 0),
        ({"status": {"restoredFilesCount": 3}}, 3),
    ],
)
def test_restored_files_count_preserves_absent_and_zero_values(
    vmfr: VirtualMachineFileRestore, instance: dict[str, Any], expected_count: int | None
) -> None:
    with patch.object(VirtualMachineFileRestore, "instance", new_callable=PropertyMock, return_value=instance):
        assert vmfr.restored_files_count == expected_count
