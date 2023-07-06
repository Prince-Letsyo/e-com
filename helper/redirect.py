from django.http import HttpResponsePermanentRedirect


class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = ['http', 'https']
