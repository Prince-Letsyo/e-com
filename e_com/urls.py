"""
URL configuration for e_com project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from user.views import PasswordTokenCheckAPI

schema_view = get_schema_view(
    openapi.Info(
        title="E-com",   
        default_version="v1",
        description="Job recuitment services",
        terms_of_service="",
        contact=openapi.Contact(email="prrinceletsyo1596.com"),
        license=openapi.License(name='BSD license')
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', schema_view.with_ui("swagger",
         cache_timeout=0), name="schema-swagger-ui"),
    path('admin/', admin.site.urls),
    path('auth/', include('user.urls')),
             path('password-reset/<uidb64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name='password_reset_confirm'),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls'))
]
