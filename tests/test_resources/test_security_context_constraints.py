import pytest

from ocp_resources.security_context_constraints import SecurityContextConstraints


@pytest.mark.incremental
class TestSecurityContextConstraints:
    @pytest.fixture(scope="class")
    def securitycontextconstraints(self, fake_client):
        return SecurityContextConstraints(
            client=fake_client,
            name="test-securitycontextconstraints",
            allow_host_dir_volume_plugin=True,
            allow_host_ipc=True,
            allow_host_network=True,
            allow_host_pid=True,
            allow_host_ports=[{"port": 80, "target_port": 8080}],
            allow_privileged_container=True,
            read_only_root_filesystem=True,
        )

    def test_01_create_securitycontextconstraints(self, securitycontextconstraints):
        """Test creating SecurityContextConstraints"""
        deployed_resource = securitycontextconstraints.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-securitycontextconstraints"
        assert securitycontextconstraints.exists

    def test_02_get_securitycontextconstraints(self, securitycontextconstraints):
        """Test getting SecurityContextConstraints"""
        assert securitycontextconstraints.instance
        assert securitycontextconstraints.kind == "SecurityContextConstraints"

    def test_03_update_securitycontextconstraints(self, securitycontextconstraints):
        """Test updating SecurityContextConstraints"""
        resource_dict = securitycontextconstraints.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        securitycontextconstraints.update(resource_dict=resource_dict)
        assert securitycontextconstraints.labels["updated"] == "true"

    def test_04_delete_securitycontextconstraints(self, securitycontextconstraints):
        """Test deleting SecurityContextConstraints"""
        securitycontextconstraints.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not securitycontextconstraints.exists
