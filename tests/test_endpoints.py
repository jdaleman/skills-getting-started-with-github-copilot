import src.app as app_module


def test_get_activities_returns_seeded_data(client):
    # Arrange
    expected_activity_count = 9

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    assert len(payload) == expected_activity_count
    assert "Chess Club" in payload
    assert "participants" in payload["Chess Club"]


def test_signup_for_activity_succeeds(client):
    # Arrange
    activity_name = "Science Club"
    email = "new-student@mergington.edu"
    initial_count = len(app_module.activities[activity_name]["participants"])

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in app_module.activities[activity_name]["participants"]
    assert len(app_module.activities[activity_name]["participants"]) == initial_count + 1


def test_signup_for_invalid_activity_returns_404(client):
    # Arrange
    invalid_activity_name = "Sky Diving"
    email = "student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{invalid_activity_name}/signup", params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_duplicate_student_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup", params={"email": existing_email}
    )

    # Assert
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Student already signed up for this activity"
    }


def test_unregister_from_activity_succeeds(client):
    # Arrange
    activity_name = "Basketball Team"
    email = "james@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup", params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {email} from {activity_name}"
    }
    assert email not in app_module.activities[activity_name]["participants"]


def test_unregister_for_invalid_activity_returns_404(client):
    # Arrange
    invalid_activity_name = "Underwater Basket Weaving"
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{invalid_activity_name}/signup", params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_non_participant_returns_400(client):
    # Arrange
    activity_name = "Drama Club"
    email = "not-enrolled@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup", params={"email": email}
    )

    # Assert
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Student is not signed up for this activity"
    }
