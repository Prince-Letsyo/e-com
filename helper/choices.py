import json
from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _

from helper.utils import filtered_cities

class Sex(TextChoices):
    MALE = "M", _("Male")
    FEMALE = "F", _("Female")



def read_data_from_file(file, filter_by):
    data = []
    try:
        with open(file, "r", encoding="utf-8")as file:
            json_data = json.load(file)
            if filter_by is not None:
                data = filtered_cities(json_data, filter_by)
            else:
                data = json_data
    except Exception as e:
        print(e)
    return data

