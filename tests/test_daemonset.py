from unittest.mock import MagicMock, patch

import pytest

from ocp_resources.daemon_set import DaemonSet


@pytest.fixture()
def daemonset(fake_client):
    return DaemonSet(client=fake_client, name="test-ds", namespace="test-ns")


def _make_instance(*, generation, observed_generation, desired, updated, available):
    """Build a mock object mimicking the structure returned by self.instance."""
    instance = MagicMock()
    instance.metadata.generation = generation
    instance.status.observedGeneration = observed_generation
    instance.status.desiredNumberScheduled = desired
    instance.status.updatedNumberScheduled = updated
    instance.status.numberAvailable = available
    instance.status.numberReady = available
    return instance


class TestWaitUntilDeployed:
    def test_wait_until_deployed_returns_when_all_ready(self, daemonset):
        ready = _make_instance(
            generation=1,
            observed_generation=1,
            desired=3,
            updated=3,
            available=3,
        )

        with patch(
            "ocp_resources.daemon_set.TimeoutSampler",
            return_value=iter([ready]),
        ):
            daemonset.wait_until_deployed(timeout=10)

    def test_wait_until_deployed_waits_when_not_all_ready(self, daemonset):
        not_ready = _make_instance(
            generation=1,
            observed_generation=1,
            desired=3,
            updated=2,
            available=2,
        )
        not_ready.status.numberReady = 2

        ready = _make_instance(
            generation=1,
            observed_generation=1,
            desired=3,
            updated=3,
            available=3,
        )

        with patch(
            "ocp_resources.daemon_set.TimeoutSampler",
            return_value=iter([not_ready, ready]),
        ):
            daemonset.wait_until_deployed(timeout=10)


class TestDelete:
    def test_delete_uses_foreground_propagation(self, daemonset):
        with patch("ocp_resources.daemon_set.super") as mock_super:
            mock_delete = MagicMock(return_value=True)
            mock_super.return_value.delete = mock_delete
            daemonset.delete(wait=True, timeout=60)

            mock_delete.assert_called_once()
            call_kwargs = mock_delete.call_args.kwargs
            assert call_kwargs["wait"] is True
            assert call_kwargs["timeout"] == 60
            assert call_kwargs["body"].propagation_policy == "Foreground"

    def test_delete_ignores_body_parameter(self, daemonset):
        with patch("ocp_resources.daemon_set.super") as mock_super:
            mock_delete = MagicMock(return_value=True)
            mock_super.return_value.delete = mock_delete
            daemonset.delete(_body={"custom": "options"})

            call_kwargs = mock_delete.call_args.kwargs
            assert call_kwargs["body"].propagation_policy == "Foreground"


class TestRollout:
    def test_rollout_patches_pod_template_annotation(self, daemonset):
        with patch.object(DaemonSet, "update") as mock_update:
            daemonset.rollout()

            mock_update.assert_called_once()
            resource_dict = mock_update.call_args.kwargs.get("resource_dict") or mock_update.call_args[1].get(
                "resource_dict"
            )

            assert resource_dict["metadata"]["name"] == "test-ds"

            annotations = resource_dict["spec"]["template"]["metadata"]["annotations"]
            assert "kubectl.kubernetes.io/restartedAt" in annotations
            assert isinstance(annotations["kubectl.kubernetes.io/restartedAt"], str)
            assert len(annotations["kubectl.kubernetes.io/restartedAt"]) > 0

    def test_rollout_calls_wait_for_rollout_when_requested(self, daemonset):
        with (
            patch.object(DaemonSet, "update"),
            patch.object(DaemonSet, "wait_for_rollout") as mock_wait,
        ):
            daemonset.rollout(wait_for_rollout=True, timeout=120)
            mock_wait.assert_called_once_with(timeout=120)

    def test_rollout_does_not_wait_by_default(self, daemonset):
        with (
            patch.object(DaemonSet, "update"),
            patch.object(DaemonSet, "wait_for_rollout") as mock_wait,
        ):
            daemonset.rollout()
            mock_wait.assert_not_called()


class TestWaitForRollout:
    def test_wait_for_rollout_returns_when_rollout_complete(self, daemonset):
        complete = _make_instance(
            generation=2,
            observed_generation=2,
            desired=3,
            updated=3,
            available=3,
        )

        with patch(
            "ocp_resources.daemon_set.TimeoutSampler",
            return_value=iter([complete]),
        ):
            daemonset.wait_for_rollout(timeout=10)

    def test_wait_for_rollout_waits_when_not_all_updated(self, daemonset):
        incomplete = _make_instance(
            generation=2,
            observed_generation=2,
            desired=3,
            updated=1,
            available=1,
        )
        complete = _make_instance(
            generation=2,
            observed_generation=2,
            desired=3,
            updated=3,
            available=3,
        )

        with patch(
            "ocp_resources.daemon_set.TimeoutSampler",
            return_value=iter([incomplete, complete]),
        ):
            daemonset.wait_for_rollout(timeout=10)

    def test_wait_for_rollout_waits_when_generation_not_observed(self, daemonset):
        stale = _make_instance(
            generation=3,
            observed_generation=2,
            desired=3,
            updated=3,
            available=3,
        )
        complete = _make_instance(
            generation=3,
            observed_generation=3,
            desired=3,
            updated=3,
            available=3,
        )

        with patch(
            "ocp_resources.daemon_set.TimeoutSampler",
            return_value=iter([stale, complete]),
        ):
            daemonset.wait_for_rollout(timeout=10)

    def test_wait_for_rollout_waits_when_not_all_available(self, daemonset):
        not_available = _make_instance(
            generation=2,
            observed_generation=2,
            desired=3,
            updated=3,
            available=1,
        )
        not_available.status.numberReady = 3

        complete = _make_instance(
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
            return_value=tracking_iter([not_available, complete]),
        ):
            daemonset.wait_for_rollout(timeout=10)

        assert len(yielded) == 2, "Expected to iterate past not-available response before completing"

    def test_wait_for_rollout_continues_when_status_missing(self, daemonset):
        no_status = MagicMock()
        no_status.status = None

        complete = _make_instance(
            generation=2,
            observed_generation=2,
            desired=3,
            updated=3,
            available=3,
        )

        with patch(
            "ocp_resources.daemon_set.TimeoutSampler",
            return_value=iter([no_status, complete]),
        ):
            daemonset.wait_for_rollout(timeout=10)

    def test_wait_for_rollout_returns_when_zero_desired(self, daemonset):
        zero_desired = _make_instance(
            generation=2,
            observed_generation=2,
            desired=0,
            updated=0,
            available=0,
        )

        with patch(
            "ocp_resources.daemon_set.TimeoutSampler",
            return_value=iter([zero_desired]),
        ):
            daemonset.wait_for_rollout(timeout=10)
