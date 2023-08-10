from django.urls import path, re_path
from dj_rest_auth.app_settings import api_settings
from user.views import (
    CustomLogoutView,
    CustomPasswordChangeView,
    CustomPasswordResetView,
    CustomPasswordResetConfirmView,
    PasswordTokenCheckAPIView,
    PasswordTokenCheckViaLinkAPIView,
    CustomUserDetailsView,
    CustomRegisterView,
    CustomVerifyEmailView,
    ConfirmEmailAPIView,
    CustomResendEmailVerificationView,
    MFAFirstStepJWTView,
    MFASecondStepJWTView,
)

auth_urlpatterns = [
    path("login/", MFAFirstStepJWTView.as_view(), name="log_in"),
    path("login/code/", MFASecondStepJWTView.as_view(), name="log_in_code"),
    path("logout/", CustomLogoutView.as_view(), name="log_out"),
    path("user/", CustomUserDetailsView.as_view(), name="user_detail"),
    re_path(
        r"^account-confirm-email/(?P<key>[-:\w]+)/$",
        ConfirmEmailAPIView.as_view(),
        name="account_confirm_email",
    ),
    path("verify-email/", CustomVerifyEmailView.as_view(), name="rest_verify_email"),
    path(
        "resend-email/",
        CustomResendEmailVerificationView.as_view(),
        name="rest_resend_email",
    ),
    path("registration/", CustomRegisterView.as_view(), name="rest_register"),
    path(
        "password-reset/",
        PasswordTokenCheckAPIView.as_view(),
        name="password_reset_confirm_no_link",
    ),
    path(
        "password-reset/<uidb64>/<token>/",
        PasswordTokenCheckViaLinkAPIView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password/change/", CustomPasswordChangeView.as_view(), name="rest_user_details"
    ),
    path(
        "password/reset/", CustomPasswordResetView.as_view(), name="rest_password_reset"
    ),
    path(
        "password/reset/confirm/",
        CustomPasswordResetConfirmView.as_view(),
        name="rest_password_reset_confirm",
    ),
]

if api_settings.USE_JWT:
    from user.views import CustomTokenVerifyView
    from user.views.api_auth.api_auth_views import CustomRefreshToken

    auth_urlpatterns += [
        path("token/verify/", CustomTokenVerifyView.as_view(), name="token_verify"),
        path("token/refresh/", CustomRefreshToken.as_view(), name="token_refresh"),
    ]
