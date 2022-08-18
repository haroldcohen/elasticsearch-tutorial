"""Here you can learn and exercise on how to search for documents"""
import elasticsearch as es
import pytest

from .fixtures import es_client, populate_es


@pytest.mark.parametrize(
    "populate_es",
    [
        {"vehicles": {
            "e9f9a60e-7f2c-4182-813f-580b30dfc85b": {
                "type": "car",
                "model": "Corvette",
                "license_plate": "1WMFG013",
                "color": "red",
                "brand": "Chevrolet",
            }
        }},
    ],
    indirect=True,
)
def test_query_match_a_car_with_license_plate_1WMFG013_should_return_a_result(es_client: es.Elasticsearch, populate_es):
    """Running this test will search for a car with said license plate"""
    result = es_client.search(
        index="vehicles",
        body={
            "query": {
                "match": {
                    "license_plate": "1WMFG013"
                }
            }
        }
    )
    expected_hits = [
        {
            "_index": "vehicles",
            "_id": "e9f9a60e-7f2c-4182-813f-580b30dfc85b",
            "_source": {
                "type": "car",
                "model": "Corvette",
                "license_plate": "1WMFG013",
                "color": "red",
                "brand": "Chevrolet",
            }
        }
    ]
    hits = result["hits"]["hits"]
    # Score can be inconsistent
    hits[0].pop("_score")
    assert result["hits"]["hits"] == expected_hits

