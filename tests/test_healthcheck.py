from fastapi.testclient import TestClient


def test_read_healthcheck(client: TestClient) -> None:
    response = client.get(
        "/healthcheck",
    )
    assert response.status_code == 200
    content = response.json()
    assert content is True
