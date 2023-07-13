from django.urls import path

from user.views.user_views import get_cites_options


user_path='user/'
user_urlpatterns = [
    path(user_path+"cities/",get_cites_options, name="user_cities")
]