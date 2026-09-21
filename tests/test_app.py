from fastapi.testclient import TestClient

from src.app import activities, app

client = TestClient(app)


def test_duplicate_signup_is_rejected():
    activity_name = "Basketball Team"
    email = "student@example.edu"
    original = activities[activity_name]["participants"][:]

    try:
        activities[activity_name]["participants"] = []

        first_response = client.post(f"/activities/{activity_name}/signup?email={email}")
        second_response = client.post(f"/activities/{activity_name}/signup?email={email}")

        assert first_response.status_code == 200
        assert second_response.status_code == 400
        assert activities[activity_name]["participants"] == [email]
    finally:
        activities[activity_name]["participants"] = original


def test_unregister_participant_removes_email():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    original = activities[activity_name]["participants"][:]

    try:
        response = client.delete(f"/activities/{activity_name}/participants/{email}")

        assert response.status_code == 200
        assert email not in activities[activity_name]["participants"]
    finally:
        activities[activity_name]["participants"] = original
