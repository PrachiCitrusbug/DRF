from rest_framework import serializers

from hms.application.user_management.services import UserAppService
from hms.domain.user_management.models import User

class AuthSerializer(serializers.Serializer):
    user_app_service = UserAppService()
    email = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(max_length=150, required=True)

    def validate(self, attr):
        """Check if user with the email exists"""
        email = attr.get("email")
        if not bool(self.user_app_service.get_user_by_email(email=email)):
            raise serializers.ValidationError("User Doesn't Exist")
        return super().validate(attr)

class PasswordForgetSerializer(serializers.Serializer):
    user_app_service = UserAppService()
    email = serializers.CharField(max_length=150, required=True)

    def validate_email(self, value):
        if value:
            if not self.user_app_service.get_user_by_email(email=value):
                raise User.DoesNotExist("User Doesn't Exist! (password forget serializer)")
            return value
        else:
            raise serializers.ValidationError("This field is required!")