from drf_yasg import openapi

site_keys = [
    openapi.Parameter(
        name="Public-Key",
        in_=openapi.IN_HEADER,
        type=openapi.TYPE_STRING,
        required=True,
    ),
    openapi.Parameter(
        name="Secret-Key",
        in_=openapi.IN_HEADER,
        type=openapi.TYPE_STRING,
        required=True,
    ),
]
non_exist_domain = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    title="Domain",
    properties={
        "domain": openapi.Schema(
            type=openapi.TYPE_STRING, default="Your domain does not exist."
        ),
    },
)

api_keys = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    title="Api-keys",
    properties={
        "Public-key": openapi.Schema(
            type=openapi.TYPE_STRING, default="Public-key is required."
        ),
        "Secret-key": openapi.Schema(
            type=openapi.TYPE_STRING, default="Secret-key is required."
        ),
    },
)
