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
