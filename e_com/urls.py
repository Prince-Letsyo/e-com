from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="E-com",   
        default_version="v1",
        description="Job recuitment services",
        terms_of_service="",
        contact=openapi.Contact(email="princeletsyo1596.com"),
        license=openapi.License(name='BSD license')
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', schema_view.with_ui("swagger",
         cache_timeout=0), name="schema-swagger-ui"),
    path('accounts/', include('allauth.account.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('user.urls')),
    path('product/', include('product.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
