import pytest
from graphene.test import Client

from src.schema import schema


@pytest.fixture
def graphql_client() -> Client:
    """Create an return a GraphQL client."""
    return Client(schema)


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "focus: mark to target specific tests and skip the rest"
    )
