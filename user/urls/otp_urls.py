from django.urls import path
from user.views.otp_views import OTPCheckPointView

otp_urlpatterns = [
    path("require_otp/", OTPCheckPointView.as_view(), name="require_otp")
]
