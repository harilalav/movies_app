from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class RequestCountTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="testpass")

    def test_get_request_count(self):
        # Simulate a GET request to fetch the request count
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("request_count"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("requests", response.data)

    def test_reset_request_count(self):
        # Simulate a POST request to reset the request count
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("reset_request_count"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "request count reset successfully")
