import pytest
from prefect.testing.utilities import prefect_test_harness

@pytest.fixture(autouse=True, scope="session")
def prefect_test_fixture():
    """
    Ensure all tests run with the Prefect test harness.
    This prevents the ephemeral server from starting and tearing down during tests,
    avoiding 'I/O operation on closed file' and timeout errors.
    """
    with prefect_test_harness():
        yield
