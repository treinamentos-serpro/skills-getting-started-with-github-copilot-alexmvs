import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture
def seeded_activities(monkeypatch):
    activities = {
        "Chess Club": {
            "participants": ["existing@mergington.edu"],
            "participant_names": {},
        }
    }
    monkeypatch.setattr(app_module, "activities", activities)
    return activities


@pytest.fixture
def client(seeded_activities):
    return TestClient(app_module.app)


def test_signup_associates_name_with_email(client, seeded_activities):
    # Arrange
    email = "ada@mergington.edu"
    name = "Ada Lovelace"

    # Act
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email, "name": name},
    )

    # Assert
    assert response.status_code == 200
    assert email in seeded_activities["Chess Club"]["participants"]
    assert seeded_activities["Chess Club"]["participant_names"][email] == name


def test_signup_rejects_duplicate_email(client, seeded_activities):
    # Arrange
    email = "existing@mergington.edu"
    original_participants = seeded_activities["Chess Club"]["participants"].copy()

    # Act
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email, "name": "Existing Student"},
    )

    # Assert
    assert response.status_code == 400
    assert seeded_activities["Chess Club"]["participants"] == original_participants


def test_signup_requires_name(client, seeded_activities):
    # Arrange
    email = "ada@mergington.edu"

    # Act
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 422
    assert email not in seeded_activities["Chess Club"]["participants"]


def test_activities_preserve_legacy_participants_without_names(client):
    # Arrange
    legacy_email = "existing@mergington.edu"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activity = response.json()["Chess Club"]
    assert legacy_email in activity["participants"]
    assert activity["participant_names"] == {}