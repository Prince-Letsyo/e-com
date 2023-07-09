from django.urls import path, re_path
from dj_rest_auth.app_settings import api_settings
from .views import (CustomLoginView,CustomLogoutView,CustomPasswordChangeView,
                    CustomPasswordResetView,CustomPasswordResetConfirmView, PasswordTokenCheckAPI, 
                    SiteCreateAPIView,CustomUserDetailsView, CustomRegisterView,
                    CustomVerifyEmailView,ConfirmEmailAPIView, CustomResendEmailVerificationView)


app_name="user"
urlpatterns = [
     path('login/', CustomLoginView.as_view(), name='log_in'),
     path('logout/', CustomLogoutView.as_view(), name='log_out'),
     path('user/', CustomUserDetailsView.as_view(), name='rest_password_reset_confirm'),
     re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailAPIView.as_view(), 
             name='account_confirm_email',),
     path('verify-email/', CustomVerifyEmailView.as_view(), name='rest_verify_email'),
    path('resend-email/', CustomResendEmailVerificationView.as_view(), name="rest_resend_email"),
     path('registration/', CustomRegisterView.as_view(), name='rest_register'),
     path('password-reset/<uidb64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name='password_reset_confirm'),
     path('password/change/', CustomPasswordChangeView.as_view(), name='rest_user_details'),
     path('password/reset/', CustomPasswordResetView.as_view(), name='rest_password_reset'),
     path('password/reset/confirm/', CustomPasswordResetConfirmView.as_view(), name='rest_password_reset_confirm'),
     path('site/', SiteCreateAPIView.as_view(), name='site'),
]

if api_settings.USE_JWT:
    from rest_framework_simplejwt.views import TokenVerifyView

    from dj_rest_auth.jwt_auth import get_refresh_view

    urlpatterns += [
        path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
        path('token/refresh/', get_refresh_view().as_view(), name='token_refresh'),
    ]
