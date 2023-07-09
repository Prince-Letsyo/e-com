from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model


# Get the UserModel
UserModel = get_user_model()

class CustomUserDetailsSerializer(UserDetailsSerializer):
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
        model = UserModel
        fields = ('pk', *extra_fields)
        read_only_fields = ('email',)