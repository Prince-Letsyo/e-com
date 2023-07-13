from django.http import JsonResponse
from helper.choices import ( read_data_from_file)


def get_cites_options(request):
    country_code = request.GET.get('country_code')
    options = {}

    if country_code:
        cities = read_data_from_file(
            file="./states.json", filter_by=country_code, type="cities")

        options = {item["state_code"]: "---------select a city---------" if item["name"]
                   == "" else item["name"] for item in cities}

    return JsonResponse(options)
