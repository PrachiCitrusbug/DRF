from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from rest_framework import serializers

from hms.application.user_management.services import UserAppService
from hms.domain.user_management.models import User, UserOTP
from lib.django.custom_models import RoleType

class AuthSerializer(serializers.Serializer):
    """serializer to verify login instance"""
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
    """serializer to verify email for password forget"""
    email = serializers.CharField(max_length=150, required=True)

class OTPSerializer(serializers.Serializer):
    """serializer to verify otp instance"""
    # user = UserListViewSerializer()
    otp = serializers.IntegerField(required=True)

    def validate_otp(self, value):
        if value:
            if value > 1000 and value < 9999:
                return value
            raise serializers.ValidationError("Otp must be of 4 digit!")
        raise serializers.ValidationError("This field is required!")

class NewPasswordSerializer(serializers.Serializer):
    """check new password"""
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        if value:
            try:
                password_validation.validate_password(value)
                return value
            except ValidationError as error:
                raise serializers.ValidationError({"new_password":str(error)})
        raise serializers.ValidationError({"new_password":"This field is required"})

class TokenSerializer(serializers.Serializer):
    """check otp token"""
    user_id = serializers.UUIDField(required=True)
    otp_token = serializers.CharField(required=True)
    new_password = NewPasswordSerializer()
    class Meta:
        model=UserOTP
        fields=['otp_token']
    
    def validate(self, attr):
        user_app_service = UserAppService()
        if not user_app_service.reset_password(attr.get('otp_token'), attr.get('user_id'), attr.get('new_password')):
            raise serializers.ValidationError({"otp_token":"Incorrect Token"})
        return super().validate(attr)
    
