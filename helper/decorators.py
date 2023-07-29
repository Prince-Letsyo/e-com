from functools import wraps
from helper.utils import *
from django.urls import reverse
from dj_rest_auth.forms import build_absolute_uri
from rest_framework.response import Response
from rest_framework import status


def fetch_data(filtered_func="filtered_"):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                filter_by = kwargs.get("filter_by", None)
                file = kwargs["file"]
                filtered = eval(filtered_func + kwargs["type"])
                kwargs["data"] = OpenFile(file, filter_by, filtered).data
                return func(*args, **kwargs)
            except Exception as e:
                raise Exception(*e.args)

        return wrapper

    return decorate


def check_domain(site_owner_model):
    def decorate(view_func):
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            public_key = request.META.get("HTTP_PUBLIC_KEY")
            secret_key = request.META.get("HTTP_SECRET_KEY")

            if public_key and secret_key:
                try:
                    site_owner_model.objects.get(
                        public_key=public_key, secret_key=secret_key
                    )
                    return view_func(self, request, *args, **kwargs)
                except site_owner_model.DoesNotExist:
                    response_data = {"domain": f"Your domain does not exist."}

            else:
                response_data = {}
                if public_key is None:
                    response_data["HTTP_PUBLIC_KEY"] = "HTTP_PUBLIC_KEY is required"
                if secret_key is None:
                    response_data["HTTP_SECRET_KEY"] = "HTTP_SECRET_KEY is required"
            return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)

        return wrapper

    return decorate
