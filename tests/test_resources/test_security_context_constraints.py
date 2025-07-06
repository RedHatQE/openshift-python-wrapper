import pytest
from fake_kubernetes_client import FakeDynamicClient
from ocp_resources.security_context_constraints import SecurityContextConstraints


class TestSecurityContextConstraints:
    @pytest.fixture(scope="class")
    def client(self):
        return FakeDynamicClient()

    @pytest.fixture(scope="class")
    def securitycontextconstraints(self, client):
        return SecurityContextConstraints(
            client=client,
            name="test-securitycontextconstraints",
            allow_host_dir_volume_plugin="test-allow_host_dir_volume_plugin",
            allow_host_ipc="test-allow_host_ipc",
            allow_host_network="test-allow_host_network",
            allow_host_pid="test-allow_host_pid",
            allow_host_ports=[{"port": 80, "target_port": 8080}],
            allow_privileged_container="test-allow_privileged_container",
            read_only_root_filesystem="test-read_only_root_filesystem",
        )

    def test_create_securitycontextconstraints(self, securitycontextconstraints):
        """Test creating SecurityContextConstraints"""
        deployed_resource = securitycontextconstraints.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-securitycontextconstraints"
        assert securitycontextconstraints.exists

    def test_get_securitycontextconstraints(self, securitycontextconstraints):
        """Test getting SecurityContextConstraints"""
        assert securitycontextconstraints.instance
        assert securitycontextconstraints.kind == "SecurityContextConstraints"

    def test_update_securitycontextconstraints(self, securitycontextconstraints):
        """Test updating SecurityContextConstraints"""
        resource_dict = securitycontextconstraints.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        securitycontextconstraints.update(resource_dict=resource_dict)
        assert securitycontextconstraints.labels["updated"] == "true"

    def test_delete_securitycontextconstraints(self, securitycontextconstraints):
        """Test deleting SecurityContextConstraints"""
        securitycontextconstraints.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not securitycontextconstraints.exists
