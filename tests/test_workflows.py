import src.app as app_module


def test_signup_then_unregister_workflow(client):
    # Arrange
    activity_name = "Debate Team"
    email = "workflow-student@mergington.edu"

    # Act
    signup_response = client.post(
        f"/activities/{activity_name}/signup", params={"email": email}
    )
    unregister_response = client.delete(
        f"/activities/{activity_name}/signup", params={"email": email}
    )

    # Assert
    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200
    assert email not in app_module.activities[activity_name]["participants"]


def test_duplicate_signup_workflow_rejects_second_attempt(client):
    # Arrange
    activity_name = "Art Studio"
    email = "duplicate-check@mergington.edu"

    # Act
    first_signup_response = client.post(
        f"/activities/{activity_name}/signup", params={"email": email}
    )
    second_signup_response = client.post(
        f"/activities/{activity_name}/signup", params={"email": email}
    )

    # Assert
    assert first_signup_response.status_code == 200
    assert second_signup_response.status_code == 400
    assert second_signup_response.json() == {
        "detail": "Student already signed up for this activity"
    }
    assert app_module.activities[activity_name]["participants"].count(email) == 1


def test_multiple_students_can_signup_to_same_activity(client):
    # Arrange
    activity_name = "Programming Class"
    new_students = [
        "multi-1@mergington.edu",
        "multi-2@mergington.edu",
        "multi-3@mergington.edu",
    ]

    # Act
    responses = [
        client.post(f"/activities/{activity_name}/signup", params={"email": email})
        for email in new_students
    ]

    # Assert
    assert all(response.status_code == 200 for response in responses)
    for email in new_students:
        assert email in app_module.activities[activity_name]["participants"]


def test_unregister_without_signup_workflow_returns_400(client):
    # Arrange
    activity_name = "Tennis Club"
    email = "never-signed-up@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup", params={"email": email}
    )

    # Assert
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Student is not signed up for this activity"
    }
