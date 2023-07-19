from django.shortcuts import render
from django.views.generic import View


class IndexView(View):
    template_name = "includes/navbar.html"
    context = {"obj": "gfhldfjkg"}

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name, context=self.context)
