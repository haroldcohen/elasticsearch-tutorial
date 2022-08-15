"""Provides with an injection fixture"""
import pytest

import elasticsearch as es


@pytest.fixture
def es_client() -> es.Elasticsearch:
    """es_client"""
    client = es.Elasticsearch(
        hosts=[
            {
                "host": "localhost",
                "port": 9200,
            }
        ],
        connection_class=es.RequestsHttpConnection,
        timeout=60,
        max_retries=10,
        retry_on_timeout=True,
        ca_certs=False,
        verify_certs=False
    )
    yield client
    for index in client.indices.get("*"):
        client.indices.delete(index=index, ignore=[400, 404])


@pytest.fixture
def populate_es(request, es_client):
    """Populates an Elasticsearch index"""
    params = request.param
    for index in params:
        for doc_id in params[index]:
            es_client.index(
                index=index,
                id=doc_id,
                body=params[index][doc_id],
                refresh=True
            )
