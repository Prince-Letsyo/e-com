from rest_framework import serializers
from user.models import UserAddress


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = [
            "id",
            "user",
            "address1",
            "address2",
            "city",
            "postal_code",
            "country",
            "telephone",
            "mobile",
        ]
