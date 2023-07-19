from .auth_urls import *
from .user_urls import *


app_name = "user"
urlpatterns = [*auth_urlpatterns, *user_urlpatterns]
