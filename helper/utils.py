import json
import validators
from allauth.account.adapter import get_current_site
from guardian.shortcuts import get_objects_for_user


class OpenFile:
    _instance = None
    data = []

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, file, filter_by, filtered):
        with open(file, "r", encoding="utf-8") as file:
            json_data = json.load(file)
            if filter_by is not None:
                data = filtered(json_data, filter_by)
            else:
                data = json_data
        OpenFile.data = data


def filtered_cities(lst, country):
    filtered_cities = []
    if country != "all":
        for city in lst:
            if city["country_code"] == country:
                filtered_cities.append(
                    {"name": city["name"], "state_code": city["state_code"]}
                )
        filtered_cities = sorted(filtered_cities, key=lambda x: x["name"])
        filtered_cities.insert(0, {"name": "", "state_code": ""})
    else:
        filtered_cities = [
            {"name": item["name"], "state_code": item["state_code"]} for item in lst
        ]
    return filtered_cities


def filtered_payment_provider(lst, type):
    filtered_provider = []
    if type != "all":
        for payment_provider in lst:
            if payment_provider["type"] == type:
                filtered_provider.append(
                    {
                        "provider": payment_provider["provider"],
                        "name": payment_provider["name"],
                    }
                )
        filtered_provider = sorted(filtered_provider, key=lambda x: x["provider"])
        filtered_provider.insert(0, {"provider": "", "name": ""})
    else:
        filtered_provider = [
            {"provider": item["provider"], "name": item["name"]} for item in lst
        ]
    return filtered_provider


def writable_nested_serializer(data, Modal, error, Serializer):
    id = data.get("id", None)
    if id:
        obj = Modal.objects.filter(id=id)
        if obj.exists():
            instance = obj.first()
            serializer = Serializer(instance=instance, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            raise error
    else:
        serializer = Serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()


def get_domain(request, site_owner_model, site):
    public_key = request.META.get("HTTP_PUBLIC_KEY")
    secret_key = request.META.get("HTTP_SECRET_KEY")

    if public_key and secret_key:
        site_owner = site_owner_model.objects.get(
            public_key=public_key, secret_key=secret_key
        )
        if site_owner:
            return get_objects_for_user(site_owner.user, ["view_site"], site).first()
    return get_current_site(request)


def is_valid_url(url):
    if validators.url(url):
        return True
    else:
        return False
