from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from hms.application.user_management.services import UserAppService
from lib.django.custom_models import RoleType


class UserListViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "email",
            "role",
            "date_joined",
            "is_staff",
            "is_active",
            "is_superuser",
        ]


class UserCreateViewSerializer(serializers.ModelSerializer):
    user_app_service = UserAppService()
    # abcd = serializers.SerializerMethodField()

    password = serializers.CharField(required=True)
    class Meta:
        model = get_user_model()
        fields = ["username", "email", "password", "role"]

    def validate_password(self, value):
        if value:
            try:
                password_validation.validate_password(value)
                return value
            except ValidationError as error:
                raise serializers.ValidationError(error)
            
    def validate_role(self, value):
        if value == RoleType.PATIENT or value == RoleType.DOCTOR:
            return value
        else:
            return RoleType.PATIENT

    def create(self, validated_data):
        role = validated_data.get("role")
        if role == RoleType.DOCTOR:
            instance = self.user_app_service.create_doctor_user(validated_data)
        else:
            instance = self.user_app_service.create_patient_user(validated_data)
        return instance
    
class UserUpdateViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = []