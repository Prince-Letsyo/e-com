from django.urls import path

from user.views.web_views import SiteOwnerUserView

web_urlpatterns = [
    path("create_domain/", SiteOwnerUserView.as_view(), name="create_domain"),
]
