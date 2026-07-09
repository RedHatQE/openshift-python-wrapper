from unittest.mock import MagicMock, patch

import pytest

from ocp_resources.daemon_set import DaemonSet


@pytest.fixture()
def daemonset(fake_client):
    return DaemonSet(client=fake_client, name="test-ds", namespace="test-ns")


def _make_api_response(*, generation, observed_generation, desired, updated, available):
    """Build a mock object mimicking the structure returned by self.api.get."""
    item = MagicMock()
    item.metadata.generation = generation
    item.status.observedGeneration = observed_generation
    item.status.desiredNumberScheduled = desired
    item.status.updatedNumberScheduled = updated
    item.status.numberAvailable = available
    item.status.numberReady = available

    response = MagicMock()
    response.items = [item]
    return response


class TestRestart:
    def test_restart_patches_pod_template_annotation(self, daemonset):
        with patch.object(DaemonSet, "update") as mock_update:
            daemonset.restart()

            mock_update.assert_called_once()
            resource_dict = mock_update.call_args.kwargs.get("resource_dict") or mock_update.call_args[1].get(
                "resource_dict"
            )

            assert resource_dict["metadata"]["name"] == "test-ds"

            annotations = resource_dict["spec"]["template"]["metadata"]["annotations"]
            assert "kubectl.kubernetes.io/restartedAt" in annotations
            assert isinstance(annotations["kubectl.kubernetes.io/restartedAt"], str)
            assert len(annotations["kubectl.kubernetes.io/restartedAt"]) > 0

    def test_restart_calls_wait_for_rollout_when_requested(self, daemonset):
        with (
            patch.object(DaemonSet, "update"),
            patch.object(DaemonSet, "wait_for_rollout") as mock_wait,
        ):
            daemonset.restart(wait_for_rollout=True, timeout=120)
            mock_wait.assert_called_once_with(timeout=120)

    def test_restart_does_not_wait_by_default(self, daemonset):
        with (
            patch.object(DaemonSet, "update"),
            patch.object(DaemonSet, "wait_for_rollout") as mock_wait,
        ):
            daemonset.restart()
            mock_wait.assert_not_called()


class TestWaitForRollout:
    def test_wait_for_rollout_returns_when_rollout_complete(self, daemonset):
        complete_response = _make_api_response(
            generation=2,
            observed_generation=2,
            desired=3,
            updated=3,
            available=3,
        )

        with patch(
            "ocp_resources.daemon_set.TimeoutSampler",
            return_value=iter([complete_response]),
        ):
            daemonset.wait_for_rollout(timeout=10)

    def test_wait_for_rollout_waits_when_not_all_updated(self, daemonset):
        incomplete_response = _make_api_response(
            generation=2,
            observed_generation=2,
            desired=3,
            updated=1,
            available=1,
        )
        complete_response = _make_api_response(
            generation=2,
            observed_generation=2,
            desired=3,
            updated=3,
            available=3,
        )

        with patch(
            "ocp_resources.daemon_set.TimeoutSampler",
            return_value=iter([incomplete_response, complete_response]),
        ):
            daemonset.wait_for_rollout(timeout=10)

    def test_wait_for_rollout_waits_when_generation_not_observed(self, daemonset):
        stale_response = _make_api_response(
            generation=3,
            observed_generation=2,
            desired=3,
            updated=3,
            available=3,
        )
        complete_response = _make_api_response(
            generation=3,
            observed_generation=3,
            desired=3,
            updated=3,
            available=3,
        )

        with patch(
            "ocp_resources.daemon_set.TimeoutSampler",
            return_value=iter([stale_response, complete_response]),
        ):
            daemonset.wait_for_rollout(timeout=10)

    def test_wait_for_rollout_waits_when_not_all_available(self, daemonset):
        not_available_response = _make_api_response(
            generation=2,
            observed_generation=2,
            desired=3,
            updated=3,
            available=1,
        )
        not_available_response.items[0].status.numberReady = 3  # ready but not available yet

        complete_response = _make_api_response(
            generation=2,
            observed_generation=2,
            desired=3,
            updated=3,
            available=3,
        )

        yielded = []

        def tracking_iter(responses):
            for r in responses:
                yielded.append(r)
                yield r

        with patch(
            "ocp_resources.daemon_set.TimeoutSampler",
            return_value=tracking_iter([not_available_response, complete_response]),
        ):
            daemonset.wait_for_rollout(timeout=10)

        assert len(yielded) == 2, "Expected to iterate past not-available response before completing"

    def test_wait_for_rollout_continues_when_status_missing(self, daemonset):
        no_status_response = MagicMock()
        no_status_response.items = [MagicMock()]
        no_status_response.items[0].status = None

        complete_response = _make_api_response(
            generation=2,
            observed_generation=2,
            desired=3,
            updated=3,
            available=3,
        )

        with patch(
            "ocp_resources.daemon_set.TimeoutSampler",
            return_value=iter([no_status_response, complete_response]),
        ):
            daemonset.wait_for_rollout(timeout=10)

    def test_wait_for_rollout_returns_when_zero_desired(self, daemonset):
        zero_desired_response = _make_api_response(
            generation=2,
            observed_generation=2,
            desired=0,
            updated=0,
            available=0,
        )

        with patch(
            "ocp_resources.daemon_set.TimeoutSampler",
            return_value=iter([zero_desired_response]),
        ):
            daemonset.wait_for_rollout(timeout=10)
