import uuid
from dataclasses import dataclass
from dataclass_type_validator import dataclass_validate
from typing import Optional
import datetime
import binascii
import os

# from django.contrib import admin
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.conf import settings
from django.utils.timezone import get_default_timezone
from django.urls import reverse_lazy

from lib.django import custom_models
from lib.django.utils import generate_otp


@dataclass(frozen=True)
class UserID:
    """
    This is a value object that should be used to generate and pass the UserID to the UserFactory
    """

    value: uuid.UUID

    
@dataclass(frozen=True)
class OtpID:
    """
    This is a value object that should be used to generate and pass the OtpID to the OtpFactory
    """

    value: uuid.UUID


@dataclass_validate
@dataclass(frozen=True)
class BaseUserParams:
    username: str
    email: str


@dataclass_validate
@dataclass(frozen=True)
class BaseUserPermissions:
    is_staff: Optional[bool] = False
    is_active: Optional[bool] = True


@dataclass_validate
@dataclass(frozen=True)
class SuperUserPermission:
    is_superuser: Optional[bool] = False




class UserManagerAutoID(UserManager):
    """User manager to create staff and superuser with auto generated id"""

    def create_staff(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("role", custom_models.RoleType.STAFF)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Staff must have is_staff=True.")
        if extra_fields.get("is_superuser") is not False:
            raise ValueError("Staff can't have superuser rights.")
        if extra_fields.get("role") != custom_models.RoleType.STAFF:
            raise ValueError("Staff must have role=staff.")
        if id not in extra_fields:
            extra_fields["id"] = UserID(uuid.uuid4()).value
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("role", custom_models.RoleType.SUPERUSER)
        if id not in extra_fields:
            extra_fields["id"] = UserID(uuid.uuid4()).value
        if extra_fields.get("role") != custom_models.RoleType.SUPERUSER:
            raise ValueError("Superuser must have role=superuser.")
        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    """Represents a User"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    role = models.CharField(
        choices=custom_models.RoleType.choices,
        max_length=10,
        default=custom_models.RoleType.PATIENT,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManagerAutoID()

    def update_entity(self, base_params:BaseUserParams, role:custom_models.RoleType, base_permissions:BaseUserPermissions, is_superuser:SuperUserPermission):
        self.username = base_params.username if base_params.username else self.username
        self.email = base_params.email if base_params.email else self.email
        self.role = role if role else self.role
        self.is_staff = base_permissions.is_staff
        self.is_active = base_permissions.is_active
        self.is_superuser = is_superuser
        self.save()
        return self
    
    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return reverse_lazy("user-detail", kwargs={"pk": self.pk})
    
    # @admin.display(description="role and is_staff?")
    # def role_staff(self):
    #     return f"{self.role.lower()} {self.is_staff}"

class UserOTP(models.Model):
    """Represents otp for user"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    otp = models.IntegerField(null=True, blank=True)
    otp_expiration = models.DateTimeField(null=True, blank=True)
    user = models.OneToOneField(null=True, to=User, on_delete=models.CASCADE)
    otp_token = models.CharField(max_length=40, null=True)
    
    def is_otp_expired(self):
        tz = get_default_timezone()
        return self.otp_expiration < datetime.datetime.now(tz=tz)


class UserFactory:
    """Factory class to create User"""

    @staticmethod
    def build_entity_with_id(
        base_params: BaseUserParams,
        role: custom_models.RoleType,
        base_permissions: BaseUserPermissions,
        is_superuser: SuperUserPermission,
    ):
        user_id = UserID(uuid.uuid4())
        return User(
            id=user_id.value,
            **BaseUserParams(**base_params).__dict__,
            role=role,
            **BaseUserPermissions(**base_permissions).__dict__,
            **SuperUserPermission(**is_superuser).__dict__,
        )

class UserOTPFactory:
    """Factory class to create otp"""
    @staticmethod
    def build_entity_with_id(user:User):
        id = OtpID(uuid.uuid4())
        otp = generate_otp()
        tz = get_default_timezone()
        otp_expiration = datetime.datetime.now(tz=tz) + datetime.timedelta(minutes=settings.OTP_EXPIRATION)
        otp_token = binascii.hexlify(os.urandom(20)).decode()
        return UserOTP(
            id=id.value,
            otp=otp,
            otp_expiration=otp_expiration,
            user=user,
            otp_token=otp_token
        )