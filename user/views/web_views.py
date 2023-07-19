from django.shortcuts import render


def index(request, *args, **kwargs):
    print(request.user)
    return render(request, "includes/navbar.html", context={})
