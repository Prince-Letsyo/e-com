from django.urls import path

from user.views import create_site_view, get_site_view, update_site_view


web_urlpatterns = [
    path("site/", get_site_view, name="get_site"),
    path("update_domain/", update_site_view, name="update_site"),
    path("create_domain/", create_site_view, name="create_domain"),
]
