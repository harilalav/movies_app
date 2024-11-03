from unittest.mock import patch

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class RegisterViewTests(APITestCase):
    def setUp(self):
        self.register_url = reverse("register")

    @patch("requests.post")
    def test_register_user_success(self, mock_post):
        # Mock the response of the token endpoint
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"access": "mocked_access_token"}

        data = {"username": "testuser", "password": "testpassword123"}
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)

        # Check if the user was created
        user_exists = User.objects.filter(username=data["username"]).exists()
        self.assertTrue(user_exists)

    @patch("requests.post")
    def test_register_user_already_exists(self, mock_post):
        User.objects.create_user(username="existinguser", password="password123")

        # Mock the response of the token endpoint
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"access": "mocked_access_token"}

        data = {"username": "existinguser", "password": "password123"}
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )  # returns access token even if user exists

    @patch("requests.post")
    def test_register_user_invalid_data(self, mock_post):
        data = {
            "username": "",  # Invalid username
            "password": "short",  # Invalid password
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This field may not be blank.", str(response.data))

    @patch("requests.post")
    def test_token_obtain_with_registered_user(self, mock_post):
        # First, register a new user
        registration_data = {"username": "testuser2", "password": "testpassword123"}
        self.client.post(self.register_url, registration_data, format="json")

        # Mock the response of the token endpoint
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"access": "mocked_access_token"}

        # Then, obtain token
        token_url = reverse("token_obtain_pair")
        token_data = {"username": "testuser2", "password": "testpassword123"}
        response = self.client.post(token_url, token_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
