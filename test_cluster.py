#!/usr/bin/env python3
"""Test DaemonSet restart() and wait_for_rollout() on a live cluster."""

from ocp_resources.daemonset import DaemonSet
from ocp_resources.namespace import Namespace
from ocp_resources.resource import get_client

client = get_client()

NS = "test-ds-restart"

# 1. Create test namespace
with Namespace(client=client, name=NS) as ns:
    ns.wait_for_status(status=Namespace.Status.ACTIVE, timeout=60)
    print(f"✅ Namespace {NS} created")

    # 2. Create a simple DaemonSet
    ds_dict = {
        "metadata": {"name": "test-ds", "namespace": NS},
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

    with DaemonSet(client=client, kind_dict=ds_dict) as ds:
        print(f"✅ DaemonSet {ds.name} created")

        # 3. Wait for initial deployment
        ds.wait_until_deployed(timeout=120)
        s = ds.instance.status
        print(f"✅ Deployed — desired={s.desiredNumberScheduled}, available={s.numberAvailable}")

        # 4. Test restart()
        print("\n--- Testing restart() ---")
        ds.restart()
        ann = ds.instance.spec.template.metadata.annotations
        print(f"✅ restartedAt: {ann.get('kubectl.kubernetes.io/restartedAt')}")
        print(f"   Generation bumped to: {ds.instance.metadata.generation}")

        # 5. Test wait_for_rollout()
        print("\n--- Testing wait_for_rollout() ---")
        ds.wait_for_rollout(timeout=300)
        s = ds.instance.status
        print(
            f"✅ Rollout complete — desired={s.desiredNumberScheduled}, "
            f"updated={s.updatedNumberScheduled}, available={s.numberAvailable}"
        )

    print("\n✅ DaemonSet cleaned up")
print(f"✅ Namespace {NS} cleaned up")
print("\n🎉 All tests passed!")
