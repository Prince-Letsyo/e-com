def filtered_cities(lst, country):
    filtered_cities = []
    if country != "all":
        for city in lst:
            if city["country_code"] == country:
                filtered_cities.append(
                    {"name": city["name"], "state_code": city["state_code"]})
        filtered_cities = sorted(filtered_cities, key=lambda x: x["name"])
        filtered_cities.insert(0, {'name': '','state_code': ''})
    else:
        filtered_cities = [{"name": item["name"], "state_code": item["state_code"]} for item in lst]
    return filtered_cities

def filtered_payment_provider(lst, type):
    filtered_cities = []
    if type != "all":
        for payment_provider in lst:
            if payment_provider["type"] == type:
                filtered_cities.append(
                    {"provider": payment_provider["provider"], "name": payment_provider["name"]})
        filtered_cities = sorted(filtered_cities, key=lambda x: x["provider"])
        filtered_cities.insert(0, {'provider': '','name': ''})
    else:
        filtered_cities = [{"provider": item["provider"], "name": item["name"]} for item in lst]
    return filtered_cities


def writable_nested_serializer(data, Modal, error, Serializer):
    id = data.get("id",None)
    if id:
        obj = Modal.objects.filter(id=id)
        if obj.exists():
            instance = obj.first()
            serializer=Serializer(instance=instance, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            raise error
    else:
        serializer = Serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()