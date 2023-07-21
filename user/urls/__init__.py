from .auth_urls import *
from .user_urls import *
from .web_urls import *


app_name = "user"
urlpatterns = [*auth_urlpatterns, *user_urlpatterns, *web_urlpatterns]
