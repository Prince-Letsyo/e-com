from django.urls import path

from user.views.web_views import create_domain


web_urlpatterns = [path("create_domain/", create_domain, name="create_domain")]
