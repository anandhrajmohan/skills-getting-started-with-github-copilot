from fastapi.testclient import TestClient

from src.app import activities, app

client = TestClient(app)


def test_duplicate_signup_is_rejected():
    original = list(activities["Chess Club"]["participants"])
    try:
        response = client.post("/activities/Chess%20Club/signup?email=michael@mergington.edu")
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"].lower()
    finally:
        activities["Chess Club"]["participants"] = original


def test_unregister_participant_removes_email():
    original = list(activities["Chess Club"]["participants"])
    try:
        activities["Chess Club"]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]
        response = client.delete("/activities/Chess%20Club/signup?email=daniel@mergington.edu")
        assert response.status_code == 200
        assert "daniel@mergington.edu" not in activities["Chess Club"]["participants"]
        assert response.json()["message"] == "Unregistered daniel@mergington.edu from Chess Club"
    finally:
        activities["Chess Club"]["participants"] = original
