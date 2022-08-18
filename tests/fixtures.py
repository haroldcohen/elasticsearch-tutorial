"""Provides with an injection fixture"""
import pytest

import elasticsearch as es


@pytest.fixture
def es_client() -> es.Elasticsearch:
    """Returns an Elasticsearch Python client instance to access the tutorial ES instance."""
    # TODO handle settings from file
    # TODO add shim like index handling to avoid unwanted deletion on es instance
    client = es.Elasticsearch(
        hosts=[
            {
                "host": "localhost",
                "port": 9200,
            }
        ],
        timeout=60,
        max_retries=10,
        retry_on_timeout=True,
        verify_certs=False,
    )
    yield client

    # Deleting test indexes from tutorial instance
    # Will be handled safely through a shim like index handling as mentioned above
    for index in client.indices.get("*"):
        client.indices.delete(index=index, ignore=[400, 404])


@pytest.fixture
def populate_es(request, es_client):
    """Populates an Elasticsearch index.
        key: The target index
        values:
            id: The id to use for indexing
            values: The json document properties

        Eg:
            [
                {
                "wizards": {
                    "1": {"first name": "Harry", "last name": "Potter"},
                    "2": {"last name": "Albus", "last name": "Dumbledore"},
                },
                "broomsticks": {
                    "1": {"model": "Nimbus 2000", "manufacturer": "Nimbus Racing Broom Company"}
                }
                }
            ]
    """
    params = request.param
    for index in params:
        for doc_id in params[index]:
            es_client.index(
                index=index,
                id=doc_id,
                body=params[index][doc_id],
                refresh=True
            )
