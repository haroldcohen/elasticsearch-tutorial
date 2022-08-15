"""Here you can learn and exercise on how to add, update and delete document"""
import elasticsearch as es
import pytest

from .fixtures import es_client, populate_es


def test_index_a_mustang_should_return_a_created_response(es_client: es.Elasticsearch):
    """Running this test will add a new mustang to the index 'vehicles'
    Feel free to play with it and change it as you please"""
    result = es_client.index(
        index="vehicles",
        body={
            "type": "car",
            "model": "mustang",
            "license_plate": "IRONMAN",
            "color": "white",
            "brand": "Ford"
        }
    )
    assert result.get("_index") == "vehicles"
    assert result.get("result") == "created"


@pytest.mark.parametrize(
    "populate_es",
    [
        {"vehicles": {
            "e9f9a60e-7f2c-4182-813f-580b30dfc85b": {
                "type": "car",
                "model": "mustang",
                "license_plate": "IRONMAN",
                "color": "white",
                "brand": "Ford"
            }
        }}
    ],
    indirect=True,
)
def test_update_a_mustang_should_return_an_updated_response(es_client: es.Elasticsearch, populate_es):
    """Running this test will update the color of the mustang license plated IRONMAN.
    Feel free to play with it and change it as you please"""
    result = es_client.update(
        index="vehicles",
        id="e9f9a60e-7f2c-4182-813f-580b30dfc85b",
        body={
            "doc": {"color": "red"}
        },
    )
    assert result.get("_index") == "vehicles"
    assert result.get("_id") == "e9f9a60e-7f2c-4182-813f-580b30dfc85b"
    assert result.get("result") == "updated"


@pytest.mark.parametrize(
    "populate_es",
    [
        {"vehicles": {
            "6c5a3e96-b9f4-4a08-ad5d-ad1fa0791d1b": {
                "type": "car",
                "model": "208",
                "license_plate": "AA123AA",
                "color": "white",
                "brand": "Peugeot"
            }
        }}
    ],
    indirect=True,
)
def test_update_a_mustang_should_return_an_updated_response(es_client: es.Elasticsearch, populate_es):
    """Running this test will update the color of the mustang license plated IRONMAN.
    Feel free to play with it and change it as you please"""
    result = es_client.delete(
        index="vehicles",
        id="6c5a3e96-b9f4-4a08-ad5d-ad1fa0791d1b",
    )
    assert result.get("_index") == "vehicles"
    assert result.get("_id") == "6c5a3e96-b9f4-4a08-ad5d-ad1fa0791d1b"
    assert result.get("result") == "deleted"
