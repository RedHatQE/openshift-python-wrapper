# import kubernetes
# import pytest
# from openshift.dynamic import DynamicClient
#
# from ocp_resources.mtv import MTV, Provider
#
#
# @pytest.fixture(scope="session")
# def client():
#     return DynamicClient(client=kubernetes.config.new_client_from_config())
#
#
# def test_provider(client):
#     pass
#     # d = MTV(name="dd", namespace="dd", client=client)
#     with Provider(
#         name="s",
#         namespace="openshift-rhmtv",
#         provider_type=Provider.ProviderType.VSPHERE,
#         secret_name="node-05",
#         secret_namespace="default",
#         client=client,
#         type=Provider.ProviderType.VSPHERE,
#         url="https://rhev-node-05.rdu2.scalelab.redhat.com/sdk",
#     ) as p:
#         p.wait_for_ready()
#     #     pass
#     #
