#!/usr/bin/env python3
"""Test DaemonSet restart() and wait_for_rollout() on a live cluster.

Tests both import paths:
  - ocp_resources.daemon_set (current module)
  - ocp_resources.daemonset (deprecated backward-compatible shim)
"""

import warnings

from ocp_resources.namespace import Namespace
from ocp_resources.resource import get_client

# --- Test 1: Import from current module ---
print("--- Testing import from ocp_resources.daemon_set ---")
from ocp_resources.daemon_set import DaemonSet  # noqa: E402

assert hasattr(DaemonSet, "restart")
assert hasattr(DaemonSet, "wait_for_rollout")
assert hasattr(DaemonSet, "wait_until_deployed")
assert hasattr(DaemonSet, "delete")
print("✅ ocp_resources.daemon_set — all methods present")

# --- Test 2: Import from deprecated module ---
print("\n--- Testing import from ocp_resources.daemonset (deprecated) ---")
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    from ocp_resources.daemonset import DaemonSet as DaemonSetOld  # noqa: E402

    assert len(w) == 1
    assert issubclass(w[0].category, DeprecationWarning)
    assert "ocp_resources.daemonset is deprecated" in str(w[0].message)
    assert DaemonSetOld is DaemonSet
    assert hasattr(DaemonSetOld, "restart")
    assert hasattr(DaemonSetOld, "wait_for_rollout")
    assert hasattr(DaemonSetOld, "wait_until_deployed")
    assert hasattr(DaemonSetOld, "delete")
    print("✅ ocp_resources.daemonset — deprecation warning raised")
    print("✅ ocp_resources.daemonset — same class, all methods present")


def run_cluster_test(ds_class, label):
    """Run the full cluster test with the given DaemonSet class."""
    print(f"\n{'=' * 60}")
    print(f"Cluster test: {label}")
    print(f"{'=' * 60}")

    client = get_client()
    ns_name = f"test-ds-{label.replace(' ', '-').lower()}"

    with Namespace(client=client, name=ns_name) as ns:
        ns.wait_for_status(status=Namespace.Status.ACTIVE, timeout=60)
        print(f"✅ Namespace {ns_name} created")

        ds_dict = {
            "metadata": {"name": "test-ds", "namespace": ns_name},
            "spec": {
                "selector": {"matchLabels": {"app": "test-ds"}},
                "template": {
                    "metadata": {"labels": {"app": "test-ds"}},
                    "spec": {
                        "containers": [
                            {
                                "name": "pause",
                                "image": "registry.k8s.io/pause:3.9",
                            }
                        ],
                        "tolerations": [{"operator": "Exists"}],
                    },
                },
            },
        }

        with ds_class(client=client, kind_dict=ds_dict) as ds:
            print(f"✅ DaemonSet {ds.name} created")

            # wait_until_deployed
            ds.wait_until_deployed(timeout=120)
            s = ds.instance.status
            print(f"✅ Deployed — desired={s.desiredNumberScheduled}, available={s.numberAvailable}")

            # restart()
            print("\n--- Testing restart() ---")
            ds.restart()
            ann = ds.instance.spec.template.metadata.annotations
            print(f"✅ restartedAt: {ann.get('kubectl.kubernetes.io/restartedAt')}")
            print(f"   Generation bumped to: {ds.instance.metadata.generation}")

            # wait_for_rollout()
            print("\n--- Testing wait_for_rollout() ---")
            ds.wait_for_rollout(timeout=300)
            s = ds.instance.status
            print(
                f"✅ Rollout complete — desired={s.desiredNumberScheduled}, "
                f"updated={s.updatedNumberScheduled}, available={s.numberAvailable}"
            )

        print("\n✅ DaemonSet cleaned up")
    print(f"✅ Namespace {ns_name} cleaned up")


# --- Cluster tests ---
run_cluster_test(DaemonSet, "daemon-set")
run_cluster_test(DaemonSetOld, "daemonset-compat")

print("\n🎉 All tests passed!")
