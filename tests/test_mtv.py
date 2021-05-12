import kubernetes
import pytest
from openshift.dynamic import DynamicClient

from ocp_resources.migration import Migration
from ocp_resources.Plan import Plan
from ocp_resources.Provider import Provider


class PlanVirtualMachineItem:
    def __init__(self, vm_name=None, vm_id=None):
        self.vm_name = vm_name
        self.vm_id = vm_id


@pytest.fixture(scope="session")
def client():
    return DynamicClient(client=kubernetes.config.new_client_from_config())


# def test_plan(client):
#     with Plan(
#         name="p",
#         namespace="openshift-mtv",
#         source_provider_name="s",
#         source_provider_namespace="openshift-mtv",
#         destination_provider_name="host",
#         destination_provider_namespace="openshift-mtv",
#         storage_map_name="node-05",
#         storage_map_namespace="openshift-mtv",
#         network_map_name="node-05",
#         network_map_namespace="openshift-mtv"
#
#
#     ) as plan:


def test_migration(client):
    # d = MTV(name="dd", namespace="dd", client=client)
    with Provider(
        name="s",
        namespace="openshift-mtv",
        provider_type=Provider.ProviderType.VSPHERE,
        secret_name="node-05",
        secret_namespace="default",
        client=client,
        url="https://rhev-node-05.rdu2.scalelab.redhat.com/sdk",
    ) as p:
        p.wait_for_condition_ready()
        with Plan(
            name="p",
            namespace="openshift-mtv",
            source_provider_name="s",
            source_provider_namespace="openshift-mtv",
            destination_provider_name="host",
            destination_provider_namespace="openshift-mtv",
            storage_map_name="node-05",
            storage_map_namespace="openshift-mtv",
            network_map_name="node-05",
            network_map_namespace="openshift-mtv",
            vms=[PlanVirtualMachineItem(vm_id="vm-333")],
        ) as plan:
            plan.wait_for_condition_ready()
            with Migration(
                name="m",
                namespace="openshift-mtv",
                plan_name="s",
                plan_namespace="openshift-mtv",
            ) as m:
                m.wait_for_condition_succeeded()
                pass

    #     pass
    #
