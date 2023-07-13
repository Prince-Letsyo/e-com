from allauth.account.models import EmailAddress
from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from helper.utils import writable_nested_serializer
from product.models.order_item import Order
from product.models.shopping_session import ShoppingSession
from product.serializers.order_serializers import OrderSerializer
from product.serializers.review_serializers import  UserReviewSessionSerializer
from product.serializers.shopping_session_serializers import  ShoppingSessionSerializer
from user.models.address import UserAddress
from user.models.payment import UserPayment


from user.serializers.address_serializers import UserAddressSerializer
from user.serializers.payment_serializers import UserPaymentSerializer

# Get the UserModel
UserModel = get_user_model()

class EmailAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model=EmailAddress
        extra_fields = []

        fields = ('id', "user","email","verified", "primary")


class CustomUserDetailsSerializer(UserDetailsSerializer):
    emailaddress_set = EmailAddressSerializer(required=False, many=True)
    useraddress = UserAddressSerializer(required=False)
    userreviewsession_set = UserReviewSessionSerializer(read_only=True,required=False,many=True)
    userpayment_set = UserPaymentSerializer(required=False, many=True)
    shoppingsession = ShoppingSessionSerializer(required=False)
    order = OrderSerializer(required=False)
    
    class Meta:
        extra_fields = []
        if hasattr(UserModel, 'USERNAME_FIELD'):
            extra_fields.append(UserModel.USERNAME_FIELD)
        if hasattr(UserModel, 'EMAIL_FIELD'):
            extra_fields.append(UserModel.EMAIL_FIELD)
        if hasattr(UserModel, 'first_name'):
            extra_fields.append('first_name')
        if hasattr(UserModel, 'last_name'):
            extra_fields.append('last_name')
        if hasattr(UserModel, 'middle_name'):
            extra_fields.append('middle_name')
        if hasattr(UserModel, 'gender'):
            extra_fields.append('gender')
        if hasattr(UserModel, 'email'):
            extra_fields.append('email')
        if hasattr(UserModel, 'useraddress'):
            extra_fields.append("useraddress")
        if hasattr(UserModel, 'userpayment_set'):
            extra_fields.append("userpayment_set")
        if hasattr(UserModel, 'shoppingsession'):
            extra_fields.append("shoppingsession")
        if hasattr(UserModel, 'userreviewsession_set'):
            extra_fields.append("userreviewsession_set")
        if hasattr(UserModel, 'emailaddress_set'):
            extra_fields.append("emailaddress_set")
        if hasattr(UserModel, 'order'):
            extra_fields.append("order")
        model = UserModel
        
        fields = ('id', *extra_fields)
        read_only_fields = ('email',)
        
    def to_internal_value(self, data):
        useraddress = data.pop("useraddress", None)
        order = data.pop("order", None)
        userpayment_set = data.pop("userpayment_set", None)
        shoppingsession = data.pop("shoppingsession", None)
        emailaddress_set = data.pop("emailaddress_set", None)

        if emailaddress_set:
            if isinstance(emailaddress_set, list):
                for emailaddress in emailaddress_set:
                    writable_nested_serializer(
                        data=emailaddress, 
                        Modal=EmailAddress, 
                        error=serializers.ValidationError(
                            {"emailaddres": "Email Address does not exist."}, 404),
                        Serializer=EmailAddressSerializer
                    )  
        if useraddress:
            writable_nested_serializer(
                data=useraddress, 
                Modal=UserAddress,
                error=serializers.ValidationError(
                    {"useraddress": "User address does not exist."}, 
                    404),
                Serializer=UserAddressSerializer
                )

        if shoppingsession:
            writable_nested_serializer(
                data=shoppingsession, 
                Modal=ShoppingSession,
                error=serializers.ValidationError(
                    {"shoppingsession": "Shopping Session does not exist."}, 
                    404),
                Serializer=ShoppingSessionSerializer
                )
            
        if order:
            writable_nested_serializer(
                data=order, 
                Modal=Order,
                error=serializers.ValidationError(
                    {"order": "User address does not exist."}, 
                    404),
                Serializer=OrderSerializer
                )

        if userpayment_set:
            if isinstance(userpayment_set, list):
                for userpayment in userpayment_set:
                    writable_nested_serializer(
                        data=userpayment, 
                        Modal=UserPayment, 
                        error=serializers.ValidationError(
                            {"userpayments": "User Payment does not exist."}, 404),
                        Serializer=UserPaymentSerializer
                    )
        return super().to_internal_value(data)

