from django.urls import path
from .views import (CustomLoginView,CustomLogoutView,CustomPasswordChangeView,
                    CustomPasswordResetView,CustomPasswordResetConfirmView, 
                    SiteCreateAPIView,CustomUserDetailsView)


app_name="user"
urlpatterns = [
     path('login/', CustomLoginView.as_view(), name='log_in'),
     path('logout/', CustomLogoutView.as_view(), name='log_out'),
     path('user/', CustomUserDetailsView.as_view(), name='rest_password_reset_confirm'),
     path('password/change/', CustomPasswordChangeView.as_view(), name='rest_user_details'),
     path('password/reset/', CustomPasswordResetView.as_view(), name='rest_password_reset'),
     path('password/reset/confirm/', CustomPasswordResetConfirmView.as_view(), name='rest_password_reset_confirm'),
     path('site/', SiteCreateAPIView.as_view(), name='site'),
]