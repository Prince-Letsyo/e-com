from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
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
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("account_login")

        if request.user.role != "SITEOWNER" and request.user.role != "ADMIN":
            return redirect("user_profile:index")

        return super(CustomSwaggerView, self).dispatch(request, *args, **kwargs)


urlpatterns = [
    path(
        "",
        include("user_profile.urls"),
    ),
    path(
        "swagger/",
        CustomSwaggerView.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc.json", CustomSwaggerView.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "redoc/",
        CustomSwaggerView.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    # path("account/", include("two_factor.urls")),
    path("accounts/", include("allauth.account.urls")),
    path("admin/", admin.site.urls),
    path("auth/", include("user.urls")),
    path("product/", include("product.urls")),
]
if settings.DEBUG:
    urlpatterns += [
        *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    ]
