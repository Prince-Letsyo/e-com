from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from dj_rest_auth.jwt_auth import JWTCookieAuthentication
from django.shortcuts import redirect
from helper.permissions import IsVerifiedSiteOwner

schema_view = get_schema_view(
    openapi.Info(
        title="E-com",
        default_version="v1",
        description="Ecommerce API",
        terms_of_service="",
        contact=openapi.Contact(email="princeletsyo1596.com"),
        license=openapi.License(name="BSD license"),
    ),
    public=True,
    permission_classes=(IsVerifiedSiteOwner,),
    authentication_classes=(
        JWTCookieAuthentication,
        SessionAuthentication,
        BasicAuthentication,
    ),
)


class CustomSwaggerView(schema_view):
    def initial(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return
        return super().initial(request, *args, **kwargs)

    def get(self, request, version="", format=None):
        if not request.user.is_authenticated:
            return redirect("account_login")
        return super().get(request, version, format)


urlpatterns = [
    path(
        "",
        CustomSwaggerView.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    # path('', include('user_profile.urls')),
    path(
        "redoc.json", CustomSwaggerView.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "redoc/",
        CustomSwaggerView.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    path("accounts/", include("allauth.account.urls")),
    path("admin/", admin.site.urls),
    path("auth/", include("user.urls")),
    path("product/", include("product.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
