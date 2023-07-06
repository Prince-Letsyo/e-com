from django.utils.translation import gettext_lazy as _
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.utils.encoding import (smart_str)
from django.utils.http import urlsafe_base64_decode
from dj_rest_auth.views import (LoginView, LogoutView, PasswordResetView, 
                                PasswordChangeView,PasswordResetConfirmView,UserDetailsView
                                )
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.exceptions import AuthenticationFailed
from helper import CustomRedirect

from user.serializers import SiteSerialiser,PasswordTokenSerializer
from user.models import User

# Create your views here.

log_in_response=openapi.Schema(
    type= openapi.TYPE_OBJECT,
    title= "CustomLogin",
    properties= {
        "access": openapi.Schema(
            title="Access",
            type=openapi.TYPE_STRING,
        ),        
        "refresh": openapi.Schema(
            title="Refresh",
            type=openapi.TYPE_STRING,
        ),        
        "user": openapi.Schema(
            title= "User",
            type=openapi.TYPE_OBJECT,
            properties= {
                    "pk": openapi.Schema(
                        title="Primary key",
                        type=openapi.TYPE_INTEGER,
                        read_only=True,
                    ),
                    "username": openapi.Schema(
                        title="User name",
                        type=openapi.TYPE_STRING
                    ),
                    "first_name": openapi.Schema(
                        title="First name",
                        type=openapi.TYPE_STRING
                    ),
                    "last_name": openapi.Schema(
                        title="Last name",
                        type=openapi.TYPE_STRING
                    ),
            },
        ),        
        "access_expiration": openapi.Schema(
            title="Access expiration",
            type=openapi.TYPE_STRING,
        ),        
        "refresh_expiration": openapi.Schema(
            title="Refresh expiration",
            type=openapi.TYPE_STRING,
        ),        
    },
)


class CustomLoginView(LoginView):
    """
    Check the credentials and return the REST Token
    if the credentials are valid and authenticated.
    Calls Django Auth login method to register User ID
    in Django session framework

    Accept the following POST parameters: username, password
    Return the REST Framework Token Object's key.
    """
    
    @swagger_auto_schema(responses={200:log_in_response},)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)



log_out_request=openapi.Schema(
    type= openapi.TYPE_OBJECT,
    title= "CustomLogout",
    properties= {
        "refresh": openapi.Schema(
            title="Refresh token",
            type=openapi.TYPE_STRING,
        ),      
    },
    required = ["refresh"]
    )

log_out_response=openapi.Schema(
    type= openapi.TYPE_OBJECT,
    title= "CustomLogout",
    properties= {
        "detail": openapi.Schema(
            type=openapi.TYPE_STRING,
            default="Successfully logged out."
        ),      
    },
    )


class CustomLogoutView(LogoutView):
    """
    Calls Django logout method and delete the Token object
    assigned to the current User object.

    Accepts/Returns nothing.
    """
    # permission_classes = (AllowAny,)
    
    @swagger_auto_schema(auto_schema=None,)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(request_body=log_out_request,responses={200: log_out_response})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    
password_change_response=openapi.Schema(
    type= openapi.TYPE_OBJECT,
    title= " CustomPasswordChange",
    properties= {
        "detail": openapi.Schema(
            type=openapi.TYPE_STRING,
            default="New password has been saved."
        ),      
    },
)


class CustomPasswordChangeView(PasswordChangeView):
    """
    Calls Django Auth SetPasswordForm save method.

    Accepts the following POST parameters: new_password1, new_password2
    Returns the success/fail message.
    """
    @swagger_auto_schema(responses={200: password_change_response})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)



password_reset_response=openapi.Schema(
    type= openapi.TYPE_OBJECT,
    title= " CustomPasswordReset",
    properties= {
        "detail": openapi.Schema(
            type=openapi.TYPE_STRING,
            default='Password reset e-mail has been sent.'
        ),      
    },
    )


class CustomPasswordResetView(PasswordResetView):
    """
    Calls Django Auth PasswordResetForm save method.

    Accepts the following POST parameters: email
    Returns the success/fail message.
    """

    @swagger_auto_schema(responses={200: password_reset_response})
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.save()
        # Return the success message with OK HTTP status
        return Response(
            data,
            status=status.HTTP_200_OK,
        )
    


password_reset_confirm_response=openapi.Schema(
    type= openapi.TYPE_OBJECT,
    title= " CustomPasswordResetConfirm",
    properties= {
        "detail": openapi.Schema(
            type=openapi.TYPE_STRING,
            default='Password has been reset with the new password.'
        ),      
    },
    )


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """
    Password reset e-mail link is confirmed, therefore
    this resets the user's password.

    Accepts the following POST parameters: token, uid,
        new_password1, new_password2
    Returns the success/fail message.
    """
    @swagger_auto_schema(responses={200: password_reset_confirm_response})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class PasswordTokenCheckAPI(GenericAPIView):
    serializer_class = PasswordTokenSerializer

    @swagger_auto_schema(auto_schema=None,)
    def get(self, request, uidb64, token):
        redirect_url = request.GET.get('redirect_url', '')
        current_site = get_current_site(request)
        valued = '?token_valid=False'
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if 'allauth' in settings.INSTALLED_APPS:
                from allauth.account.forms import default_token_generator
            else:
                from django.contrib.auth.tokens import default_token_generator
                
            if not default_token_generator.check_token(user, token):
                if redirect_url and len(redirect_url) > 3:
                    return CustomRedirect(f'{redirect_url}{valued}')
                else:
                    return CustomRedirect(f'{current_site}{valued}')
            else:
                valued = f'?token_valid=True&message=Credential_valid&uidb64={uidb64}&token={token}'
                if redirect_url and len(redirect_url) > 3:
                    return CustomRedirect(f'{redirect_url}{valued}')
                else:
                    return CustomRedirect(f'{current_site}{valued}')

        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)

    def post(self, request, uidb64, token):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({"success": True, 'token': serializer.data['token'],
                         'uidb64': serializer.data['uidb64']},
                        status=status.HTTP_200_OK)


class SiteCreateAPIView(CreateAPIView):
    serializer_class = SiteSerialiser

class CustomUserDetailsView(UserDetailsView):
    pass