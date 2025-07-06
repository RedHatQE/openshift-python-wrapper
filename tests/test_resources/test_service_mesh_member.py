import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.service_mesh_member import ServiceMeshMember


@pytest.mark.incremental
class TestServiceMeshMember:
    @pytest.fixture(scope="class")
    def client(self):
        return FakeDynamicClient()

    @pytest.fixture(scope="class")
    def servicemeshmember(self, client):
        return ServiceMeshMember(
            client=client,
            name="test-servicemeshmember",
            namespace="default",
            control_plane_ref={"test-control_plane_ref": "test-value"},
        )

    def test_01_create_servicemeshmember(self, servicemeshmember):
        """Test creating ServiceMeshMember"""
        deployed_resource = servicemeshmember.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-servicemeshmember"
        assert servicemeshmember.exists

    def test_02_get_servicemeshmember(self, servicemeshmember):
        """Test getting ServiceMeshMember"""
        assert servicemeshmember.instance
        assert servicemeshmember.kind == "ServiceMeshMember"

    def test_03_update_servicemeshmember(self, servicemeshmember):
        """Test updating ServiceMeshMember"""
        resource_dict = servicemeshmember.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        servicemeshmember.update(resource_dict=resource_dict)
        assert servicemeshmember.labels["updated"] == "true"

    def test_04_delete_servicemeshmember(self, servicemeshmember):
        """Test deleting ServiceMeshMember"""
        servicemeshmember.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not servicemeshmember.exists
