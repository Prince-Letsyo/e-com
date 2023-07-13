import json

from rest_framework import renderers


class MainRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_data = {}
        if renderer_context and "response" in renderer_context:
            response = renderer_context["response"]
            if response.exception or response.status_code >= 400:
                response_data ={"error": data}
            else:
                response_data = {"data": data}
        else:
            response_data = {"data": data}

        return super().render(response_data, accepted_media_type, renderer_context)
