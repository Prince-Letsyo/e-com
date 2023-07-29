from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class APITestSetUp(APITestCase):
    def setUp(self):
        self.public_key = ""
        self.secret_key = ""
        self.csrftoken = ""
        self.site = {"domain": "http://www.go.com", "name": "www.go.com"}
        self.site_ = '{"domain": "http://www.go.com", "name": "www.go.com"}'
        self.register_url_siteowner = reverse("account_signup")
        self.log_in_url_siteownwer = reverse("account_login")
        self.create_domain = reverse("user:create_domain", current_app="user")
        self.register_url = reverse("user:rest_register", current_app="user")
        self.log_in_url = reverse("user:log_in", current_app="user")
        self.register_siteowner_credentials = {
            "username": "string",
            "email": "user@example.com",
            "password1": "ingstr2402GHWOS",
            "password2": "ingstr2402GHWOS",
            "first_name": "string",
            "last_name": "string",
            "middle_name": "string",
            "gender": "M",
        }
        self.register_credentials = {
            "username": "stringgsg",
            "email": "usefgasdfagr@example.com",
            "password1": "ingstr2dfgd402GHWOS",
            "password2": "ingstr2dfgd402GHWOS",
            "first_name": "strfsfsing",
            "last_name": "strisdng",
            "middle_name": "strsding",
            "gender": "M",
        }
        return super().setUp()

    def tearDown(self):
        return super().tearDown()
