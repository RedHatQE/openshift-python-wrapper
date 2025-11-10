import pytest

from ocp_resources.resource import get_client


@pytest.fixture(scope="class")
def fake_client():
    """Fixture that provides a fake client for testing"""
    return get_client(fake=True)


def pytest_runtest_makereport(item, call):
    """
    incremental tests implementation
    """
    if call.excinfo is not None and "incremental" in item.keywords:
        parent = item.parent
        parent._previousfailed = item


def pytest_runtest_setup(item):
    """
    Use incremental
    """

    if "incremental" in item.keywords:
        previousfailed = getattr(item.parent, "_previousfailed", None)
        if previousfailed is not None:
            pytest.xfail(f"previous test failed ({previousfailed.name})")
