import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    ("query_param", "expected_q"),
    [
        (None, None),  # without query parameter
        ("somequery", "somequery"),  # with query parameter
    ],
    ids=["without_query", "with_query"],
)
def test_read_item(
    client: TestClient, query_param: str | None, expected_q: str | None
) -> None:
    """Test reading an item with and without query parameter."""
    item_id = 5
    url = f"/items/{item_id}"
    if query_param is not None:
        url += f"?q={query_param}"

    response = client.get(url)
    assert response.status_code == 200
    content = response.json()
    assert content["item_id"] == item_id
    assert content["q"] == expected_q
