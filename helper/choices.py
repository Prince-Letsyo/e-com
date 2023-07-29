from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _

from helper.decorators import fetch_data


class Sex(TextChoices):
    MALE = "M", _("Male")
    FEMALE = "F", _("Female")


class PaymentType(TextChoices):
    BANK = "bank", _("Bank")
    MOMO = "momo", _("Mobile money")


class DeliveryType(TextChoices):
    STANDARDDELIVERY = "standard_delivery", _("Standard delivery")
    EXPRESSDELIVERY = "express_delivery", _("Express delivery")
    INTERNATIONALDELIVERY = "international_delivery", _("International delivery")
    INSTOREPICKUP = "in_store_pick_up", _("In-Store Pickup")


class ShippingType(TextChoices):
    POSTALSERVICE = "postal_service", _("Postal Service")
    COURIERSERVICES = "courier_services", _("Couriers Services")


class PromotionType(TextChoices):
    DISCOUNT = "discount", _("Discount")
    COUPONCODE = "coupon_code", _("Coupon Code")
    FREESHIPPING = "free_shipping", _("Free Shipping")
    FLASHSALE = "flash_sale", _("Flash Sale")


class StatusOrder(TextChoices):
    PACKAGING = "Packaging", _("Packaging")
    PROCESSING = "processing", _("Processing")
    DISPATCHING = "dispatching", _("Dispatching")
    SHIPPING = "shipping", _("Shipping")
    DELIVERY = "delivery", _("Delivery")


@fetch_data()
def read_data_from_file(file, filter_by, type, data=[]):
    return data


@fetch_data()
def make_choices_data(file, key, value, type, filter_by=None, data=[]):
    choices_data = [
        ("", "---------select---------")
        if filter_by
        else ("---------select---------", "")
    ]

    if filter_by == "all":
        choices_data = []

    for x in [
        (item[value] if filter_by else item[value], _(item[key])) for item in data
    ]:
        if filter_by and (x[1] != "" and x[0] != ""):
            choices_data.append(x)
        elif filter_by is None:
            choices_data.append(x)
    return choices_data


city_choices = make_choices_data(
    key="name", value="state_code", type="cities", file="./states.json", filter_by="all"
)
payment_provider_choices = make_choices_data(
    key="provider",
    value="name",
    type="payment_provider",
    file="./payment_providers.json",
    filter_by="all",
)
