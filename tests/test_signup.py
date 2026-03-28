import unittest
from copy import deepcopy

from fastapi.testclient import TestClient

from src.app import activities, app


class SignupTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.original_activities = deepcopy(activities)

    def tearDown(self):
        activities.clear()
        activities.update(deepcopy(self.original_activities))

    def test_duplicate_signup_returns_conflict(self):
        response = self.client.post(
            "/activities/Chess%20Club/signup",
            params={"email": "michael@mergington.edu"},
        )

        self.assertEqual(response.status_code, 409)
        self.assertEqual(
            response.json()["detail"],
            "Student is already signed up for this activity",
        )
        self.assertEqual(
            activities["Chess Club"]["participants"].count("michael@mergington.edu"),
            1,
        )

    def test_successful_signup_normalizes_email(self):
        response = self.client.post(
            "/activities/Chess%20Club/signup",
            params={"email": "  newstudent@mergington.edu  "},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("newstudent@mergington.edu", activities["Chess Club"]["participants"])

    def test_unregister_removes_existing_participant(self):
        response = self.client.delete(
            "/activities/Chess%20Club/participants",
            params={"email": "michael@mergington.edu"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("michael@mergington.edu", activities["Chess Club"]["participants"])

    def test_unregister_missing_participant_returns_not_found(self):
        response = self.client.delete(
            "/activities/Chess%20Club/participants",
            params={"email": "not-registered@mergington.edu"},
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["detail"],
            "Student is not signed up for this activity",
        )


if __name__ == "__main__":
    unittest.main()
