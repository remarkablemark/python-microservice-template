from fastapi.testclient import TestClient


def test_read_item(client: TestClient) -> None:
    item_id = 5
    response = client.get(
        f"/items/{item_id}",
    )
    assert response.status_code == 200
    content = response.json()
    assert content["item_id"] == item_id
    assert content["q"] is None


def test_read_item_and_querystring(client: TestClient) -> None:
    item_id = 5
    query_value = "somequery"
    response = client.get(
        f"/items/{item_id}?q={query_value}",
    )
    assert response.status_code == 200
    content = response.json()
    assert content["item_id"] == item_id
    assert content["q"] == query_value
