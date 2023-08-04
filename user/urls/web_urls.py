from django.urls import path
from user.views.json_web_views import (
    create_user_token_device,
    create_site_view,
    get_site_view,
    update_site_view,
    json_token_check_view,
    create_backup_token_code_view,
)
from user.views.web_views import qrcode_view

web_urlpatterns = [
    path("site/", get_site_view, name="get_site"),
    path("update_domain/", update_site_view, name="update_site"),
    path("create_domain/", create_site_view, name="create_domain"),
    path("token_setup/", create_user_token_device, name="token_setup"),
    path("token_setup/check/", json_token_check_view, name="json_token_check"),
    path(
        "token_setup/backup_code/",
        create_backup_token_code_view,
        name="create_backup_token_code",
    ),
    path("token_setup/qrcode/<int:pk>/<str:device_type>/", qrcode_view, name="qrcode"),
]
