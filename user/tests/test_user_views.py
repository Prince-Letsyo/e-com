import json
import pprint
from django.conf import settings
from django.db.models import Q
from django.urls import reverse
from rest_framework import status
from helper.test_setup import APITestSetUp
from django.contrib.sites.models import Site
from guardian.shortcuts import get_objects_for_user
from user.models import User, SiteOwnerProfile
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode
from allauth.account.models import EmailAddress


if "allauth" in settings.INSTALLED_APPS:
    from allauth.account.forms import default_token_generator
    from allauth.account.utils import (
        user_pk_to_url_str,
    )


# Create your tests here.
class TestUserTest(APITestSetUp):
    def sign_up_siteoewner(self):
        pass

    @property
    def siteowner_object(self):
        return User.objects.get(
            username=self.register_siteowner_credentials["username"]
        )

    def test_signup_siteowner(self):
        res = self.client.post(
            self.register_url_siteowner, self.register_siteowner_credentials
        )
        person = self.siteowner_object
        person_email = EmailAddress.objects.filter(
            Q(user=person) & Q(primary=True)
        ).first()
        person_email.verified = True
        person_email.save()
        self.csrftoken = res.cookies["csrftoken"].value
        self.assertEqual(person.role, "SITEOWNER")
        self.assertEqual(
            res.url, reverse("user_profile:profile", current_app="user_profile")
        )
        self.assertRedirects(
            res, reverse("user_profile:profile", current_app="user_profile")
        )
        self.assertEqual(res.status_code, status.HTTP_302_FOUND)

    def generate_password_reset_link(self):
        self.test_siteowner_has_profile()
        user = self.siteowner_object
        temp_key = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(smart_bytes(user_pk_to_url_str(user)))
        return uid, temp_key

    def test_siteowner_can_reset_via_json(self):
        uid, temp_key = self.generate_password_reset_link()
        res = self.client.post(
            reverse(
                "user:password_reset_confirm", args=[uid, temp_key], current_app="user"
            ),
            {"uidb64": uid, "token": temp_key},
            headers={
                "Public-key": self.public_key,
                "Secret-key": self.secret_key,
                "x-csrftoken": self.secret_key,
            },
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_siteowner_can_reset_password(self):
        uid, temp_key = self.generate_password_reset_link()
        res = self.client.get(
            reverse(
                "user:password_reset_confirm", args=[uid, temp_key], current_app="user"
            )
        )
        self.assertEqual(res.status_code, status.HTTP_301_MOVED_PERMANENTLY)

    def test_siteowner_has_profile(self):
        self.test_signup_siteowner()
        person = self.siteowner_object
        site_owner = SiteOwnerProfile.objects.get(user=person)
        self.assertEqual(person, site_owner.user)
        self.public_key = site_owner.public_key
        self.secret_key = site_owner.secret_key

    def test_siteowner_can_login(self):
        self.test_siteowner_has_profile()
        res = self.client.post(
            self.log_in_url_siteownwer,
            {
                "username": self.register_siteowner_credentials["username"],
                "password": self.register_siteowner_credentials["password1"],
            },
        )
        self.assertEqual(
            res.url, reverse("user_profile:profile", current_app="user_profile")
        )
        self.assertRedirects(
            res, reverse("user_profile:profile", current_app="user_profile")
        )
        self.assertEqual(res.status_code, status.HTTP_302_FOUND)

    def test_add_site_by_siteowner(self):
        self.test_siteowner_can_login()
        res = self.client.post(
            self.create_domain,
            json.dumps(self.site).encode(),
            content_type="application/json",
        )
        self.assertDictEqual(res.json(), self.site)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_siteowner_has_site(self):
        self.test_add_site_by_siteowner()
        user = self.siteowner_object
        site = Site.objects.get(domain=self.site["domain"])
        owner_site = get_objects_for_user(user, ["view_site"], Site).first()
        self.assertEqual(owner_site, site)

    def test_user_can_register(self):
        self.test_siteowner_has_site()
        headers = {
            "Public-key": self.public_key,
            "Secret-key": self.secret_key,
            "x-csrftoken": self.secret_key,
        }
        res = self.client.post(
            self.register_url, self.register_credentials, headers=headers
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_user_can_login(self):
        self.test_user_can_register()
        headers = {
            "Public-key": self.public_key,
            "Secret-key": self.secret_key,
            "x-csrftoken": self.secret_key,
        }
        res = self.client.post(
            self.log_in_url,
            {
                "username": self.register_credentials["username"],
                "password": self.register_credentials["password1"],
            },
            headers=headers,
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
