import pytest

from ocp_resources.dns_operator_openshift_io import DNS


@pytest.mark.incremental
class TestDNS:
    @pytest.fixture(scope="class")
    def dns(self, fake_client):
        return DNS(
            client=fake_client,
            name="test-dns",
        )

    def test_01_create_dns(self, dns):
        """Test creating DNS"""
        deployed_resource = dns.deploy()
        assert deployed_resource
        assert deployed_resource.name == "test-dns"
        assert dns.exists

    def test_02_get_dns(self, dns):
        """Test getting DNS"""
        assert dns.instance
        assert dns.kind == "DNS"

    def test_03_update_dns(self, dns):
        """Test updating DNS"""
        resource_dict = dns.instance.to_dict()
        resource_dict["metadata"]["labels"] = {"updated": "true"}
        dns.update(resource_dict=resource_dict)
        assert dns.labels["updated"] == "true"

    def test_04_delete_dns(self, dns):
        """Test deleting DNS"""
        dns.clean_up(wait=False)
        # Verify resource no longer exists after deletion
        assert not dns.exists
