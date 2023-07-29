from django.urls import path

from user_profile.views import IndexTemplateView, ProfileTemplateView

app_name = "user_profile"

urlpatterns = [
    path("", IndexTemplateView.as_view(), name="index"),
    path("accounts/profile/", ProfileTemplateView.as_view(), name="profile"),
]
