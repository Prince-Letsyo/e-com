from abc import ABC, abstractmethod
from dj_rest_auth.views import api_settings
from dj_rest_auth.views import LoginView
from dj_rest_auth.app_settings import api_settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_401_UNAUTHORIZED,
)
from trench.command.authenticate_user import authenticate_user_command
from trench.command.authenticate_second_factor import authenticate_second_step_command
from trench.exceptions import MFAMethodDoesNotExistError, MFAValidationError
from trench.utils import get_mfa_model, user_token_generator
from trench.backends.provider import get_mfa_handler
from trench.responses import ErrorResponse
from trench.serializers import (
    LoginSerializer,
    CodeLoginSerializer,
)
from helper.decorators import check_domain
from user.serializers import (
    LogInResponseWithExpirationSerializer,
    LogInResponseWithoutExpirationSerializer,
)
from user.models import User, SiteOwnerProfile
from user.serializers.auth_serializers import AllauthCodeLoginSerializer
from user.views.views_utils import *


class MFAStepMixin(LoginView, ABC):
    @abstractmethod
    def _successful_authentication_response(self) -> Response:
        raise NotImplementedError


class MFAFirstStepMixin(MFAStepMixin, ABC):
    @check_domain(site_owner_model=SiteOwnerProfile)
    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            200: LogInResponseWithExpirationSerializer
            if api_settings.JWT_AUTH_RETURN_EXPIRATION
            else LogInResponseWithoutExpirationSerializer,
            401: non_exist_domain,
            403: api_keys,
        },
        manual_parameters=site_keys,
    )
    def post(self, request) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = authenticate_user_command(
                request=request,
                username=serializer.validated_data[User.USERNAME_FIELD],
                password=serializer.validated_data["password"],
            )
        except MFAValidationError as cause:
            return ErrorResponse(error=cause)
        try:
            mfa_model = get_mfa_model()
            mfa_method = mfa_model.objects.get_primary_active(user_id=user.id)
            get_mfa_handler(mfa_method=mfa_method).dispatch_message()
            return Response(
                data={
                    "ephemeral_token": user_token_generator.make_token(user),
                    "method": mfa_method.name,
                }
            )
        except MFAMethodDoesNotExistError:
            return self._successful_authentication_response(request)


class MFASecondStepMixin(MFAStepMixin, ABC):
    @check_domain(site_owner_model=SiteOwnerProfile)
    @swagger_auto_schema(
        request_body=AllauthCodeLoginSerializer,
        responses={
            200: LogInResponseWithExpirationSerializer
            if api_settings.JWT_AUTH_RETURN_EXPIRATION
            else LogInResponseWithoutExpirationSerializer,
            401: non_exist_domain,
            403: api_keys,
        },
        manual_parameters=site_keys,
    )
    def post(self, request) -> Response:
        serializer = CodeLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            authenticate_second_step_command(
                code=serializer.validated_data["code"],
                ephemeral_token=serializer.validated_data["ephemeral_token"],
            )
            return self._successful_authentication_response(request)
        except MFAValidationError as cause:
            return ErrorResponse(error=cause, status=HTTP_401_UNAUTHORIZED)


class MFAJWTView(MFAStepMixin):
    def _successful_authentication_response(self, request) -> Response:
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data)
        self.serializer.is_valid(raise_exception=True)

        self.login()
        return self.get_response()


class MFAFirstStepJWTView(MFAJWTView, MFAFirstStepMixin):
    pass


class MFASecondStepJWTView(MFAJWTView, MFASecondStepMixin):
    pass
