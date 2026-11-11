import pytest

from app.main import create_app


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    return create_app().test_client()


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_cards_start_empty(client):
    assert client.get("/cards").get_json() == []


def test_add_card(client):
    response = client.post("/cards", json={"front": "pod", "back": "smallest k8s unit"})
    assert response.status_code == 201
    assert client.get("/cards").get_json() == [
        {"id": 1, "front": "pod", "back": "smallest k8s unit"}
    ]


def test_add_card_requires_front_and_back(client):
    assert client.post("/cards", json={"front": "pod"}).status_code == 400
