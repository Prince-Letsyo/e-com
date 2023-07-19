from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse


class TestSetUp(APITestCase):
    def test_user_cannot_register_with_no_data(self):
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_register(self):
        res = self.client.post(self.register_url, self.register_credentials)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def setUp(self):
        self.register_url = reverse("user:rest_register", current_app="user")
        self.log_in_url = reverse("user:log_in", current_app="user")
        self.register_credentials = {
            "username": "string",
            "email": "user@example.com",
            "password1": "ingstr2402GHWOS",
            "password2": "ingstr2402GHWOS",
            "first_name": "string",
            "last_name": "string",
            "middle_name": "string",
            "gender": "M",
            # "site": "http://example.com"
        }
        return super().setUp()

    def tearDown(self):
        return super().tearDown()
