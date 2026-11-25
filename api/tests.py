from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()


class HealthcareApiTests(APITestCase):
    def test_register_and_login(self):
        register_response = self.client.post(
            "/api/auth/register/",
            {
                "name": "Test User",
                "email": "test@example.com",
                "password": "TestPassword123!",
            },
            format="json",
        )
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)

        login_response = self.client.post(
            "/api/auth/login/",
            {"email": "test@example.com", "password": "TestPassword123!"},
            format="json",
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", login_response.data)

    def test_patient_requires_login_and_is_private(self):
        response = self.client.get("/api/patients/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        user = User.objects.create_user(
            email="owner@example.com",
            password="TestPassword123!",
            name="Owner",
        )
        self.client.force_authenticate(user=user)
        create_response = self.client.post(
            "/api/patients/",
            {"name": "Patient One", "age": 30, "gender": "Other"},
            format="json",
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.client.get("/api/patients/").status_code, status.HTTP_200_OK)
