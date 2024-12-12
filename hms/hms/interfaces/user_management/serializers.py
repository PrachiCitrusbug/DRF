from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from lib.django.custom_exceptions import SerializerException
from hms.application.user_management.services import UserAppService


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

    password = serializers.CharField(required=False)

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "password", "role"]

    def validate_password(self, value):
        if self.instance:
            if value:
                raise serializers.ValidationError({"password":"Password field cannot be changed"})
            return None
        else:
            if value:
                try:
                    password_validation.validate_password(value)
                    return value
                except ValidationError as error:
                    raise serializers.ValidationError({"password":str(error)})
            raise serializers.ValidationError({"password":"This field is required"})
    
    def validate(self, attr):
        value = None
        if attr.get("password"):
            value = attr.get("password")
        self.validate_password(value)
        return super().validate(attr)

    def create(self, validated_data):
        try:
            instance = self.user_app_service.create_user(validated_data)
            return instance
        except Exception as e:
            raise SerializerException(f"{e} at create() in UserCreateViewSerializer")

    def update(self, instance, validated_data):
        try:
            # TODO : Try this
            # instance.username = validated_data.get("username") if validated_data.get("username") else instance.username
            # instance.email = validated_data.get("email") if validated_data.get("email") else instance.email
            # instance.role = validated_data.get("role") if validated_data.get("role") else instance.role
            instance.__dict__.update(**validated_data)
            instance = self.user_app_service.update_user(instance)
            return instance
        except Exception as e:
            raise SerializerException(
                f"{e} at update() in UserCreateViewSerializer"
            )


class UserUpdateViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = []
