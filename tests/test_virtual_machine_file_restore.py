from collections.abc import Callable, Iterator
from typing import Any
from unittest.mock import MagicMock, PropertyMock, call, patch

import pytest
from kubernetes.client.rest import ApiException
from kubernetes.dynamic.exceptions import ForbiddenError, InternalServerError, NotFoundError, ServerTimeoutError
from timeout_sampler import TimeoutExpiredError
from urllib3.exceptions import ProtocolError

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
def test_wait_for_phase_waits_through_intermediate_phases(
    vmfr: VirtualMachineFileRestore, vmfr_api: MagicMock, target_phase: str
) -> None:
    vmfr_api.get.side_effect = [{}, {"status": {"phase": "Init"}}, {"status": {"phase": target_phase}}]
    vmfr.wait_for_phase(target_phase=target_phase, timeout=1, sleep=0)
    assert vmfr_api.get.call_count == 3


@pytest.mark.parametrize(
    "read_error",
    [
        ProtocolError("Connection aborted"),
        NotFoundError(ApiException(status=404, reason="Restore not found yet")),
        ConnectionResetError("Connection reset"),
        InternalServerError(ApiException(status=500, reason="etcdserver: leader changed")),
        ServerTimeoutError(ApiException(status=504, reason="Server timed out")),
        ForbiddenError(ApiException(status=403, reason="context deadline exceeded")),
    ],
    ids=["protocol", "not-found", "connection-reset", "etcd-leader-change", "server-timeout", "deadline-exceeded"],
)
def test_wait_for_phase_retries_transient_reads(
    vmfr: VirtualMachineFileRestore, vmfr_api: MagicMock, read_error: Exception
) -> None:
    vmfr_api.get.side_effect = [read_error, {"status": {"phase": "Succeeded"}}]
    vmfr.wait_for_phase(target_phase=vmfr.Phase.SUCCEEDED, timeout=1, sleep=0)
    assert vmfr_api.get.call_count == 2


@pytest.mark.parametrize(
    "read_error",
    [
        ForbiddenError(ApiException(status=403, reason="Permission denied")),
        InternalServerError(ApiException(status=500, reason="Non-transient server error")),
        ValueError("Invalid response"),
    ],
    ids=["permission-denied", "unmatched-server-error", "invalid-response"],
)
def test_wait_for_phase_does_not_retry_unmatched_read_errors(
    vmfr: VirtualMachineFileRestore, vmfr_api: MagicMock, read_error: Exception
) -> None:
    """Unmatched reads fail immediately through the sampler, preserving the original error."""
    vmfr_api.get.side_effect = [read_error, {"status": {"phase": "Succeeded"}}]
    with pytest.raises(TimeoutExpiredError) as error:
        vmfr.wait_for_phase(target_phase=vmfr.Phase.SUCCEEDED, timeout=1, sleep=0)
    assert error.value.last_exp is read_error
    assert vmfr_api.get.call_count == 1


def test_wait_for_phase_reports_failure_details(vmfr: VirtualMachineFileRestore, vmfr_api: MagicMock) -> None:
    vmfr_api.get.return_value = {"status": {"phase": "Failed", "errorMessage": "Backup snapshot is missing"}}
    with pytest.raises(RuntimeError, match="test-restore.*Backup snapshot is missing"):
        vmfr.wait_for_phase(target_phase=vmfr.Phase.SUCCEEDED, timeout=1, sleep=0)


def test_wait_for_phase_allows_expected_failure(vmfr: VirtualMachineFileRestore, vmfr_api: MagicMock) -> None:
    vmfr_api.get.return_value = {"status": {"phase": "Failed"}}
    vmfr.wait_for_phase(target_phase=vmfr.Phase.FAILED, timeout=1, sleep=0)


def test_wait_for_phase_times_out(vmfr: VirtualMachineFileRestore, vmfr_api: MagicMock) -> None:
    vmfr_api.get.return_value = {"status": {"phase": "Restoring"}}
    with pytest.raises(TimeoutExpiredError):
        vmfr.wait_for_phase(target_phase=vmfr.Phase.SUCCEEDED, timeout=0, sleep=0)
    vmfr_api.get.assert_not_called()


@pytest.fixture()
def vmfr_api(vmfr: VirtualMachineFileRestore) -> Iterator[MagicMock]:
    with patch.object(VirtualMachineFileRestore, "api", new_callable=PropertyMock) as api:
        yield api.return_value


def test_wait_for_phase_uses_one_retry_budget(vmfr: VirtualMachineFileRestore, vmfr_api: MagicMock) -> None:
    """Repeated cluster errors consume only the phase budget, without the instance retry loop."""
    elapsed = 0.0

    def advance_time(seconds: float) -> None:
        nonlocal elapsed
        elapsed += seconds

    read_error = InternalServerError(ApiException(status=500, reason="etcdserver: leader changed"))
    vmfr_api.get.side_effect = read_error
    with (
        patch("timeout_sampler.time.time", side_effect=lambda: elapsed),
        patch("timeout_sampler.time.sleep", side_effect=advance_time),
    ):
        with pytest.raises(TimeoutExpiredError):
            vmfr.wait_for_phase(target_phase=vmfr.Phase.SUCCEEDED, timeout=2, sleep=1)

    assert elapsed == 2
    assert vmfr_api.get.call_args_list == [call(name=vmfr.name, namespace=vmfr.namespace)] * 2


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
