import uuid
from dataclasses import dataclass
from dataclass_type_validator import dataclass_validate

from django.contrib import admin
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from lib.django import custom_models

@dataclass(frozen=True)
class UserID:
    """
    This is a value object that should be used to generate and pass the UserID to the UserFactory
    """
    value: uuid.UUID

@dataclass_validate
@dataclass(frozen=True)
class BaseUserParams:
    username:str
    email:str

@dataclass_validate
@dataclass(frozen=True)
class BaseUserPermissions:
    is_staff: bool
    is_active: bool

class UserManagerAutoID(UserManager):
    """ User manager to create staff and superuser with auto generated id """
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
    """ Represents a User """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        verbose_name="email address", max_length=255, unique=True)
    role = models.CharField(choices=custom_models.RoleType.choices, max_length=10, default=custom_models.RoleType.PATIENT)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManagerAutoID()
    def update_entity(self, base_params: BaseUserParams, role:custom_models.RoleType, base_permissions:BaseUserPermissions):
        self.username = base_params.username if base_params.username else self.username
        self.email = base_params.email if base_params.email else self.email
        self.role = role if role else self.role
        self.is_staff = base_permissions.is_staff
        self.is_active = base_permissions.is_active
        self.save()
        return self

    @admin.display(description="role and is_staff?")
    def role_staff(self):
        return f"{self.role.lower()} {self.is_staff}"

class UserFactory:
    """Factory class to create User"""

    @staticmethod
    def build_entity_with_id(base_params: BaseUserParams, role:custom_models.RoleType=custom_models.RoleType.PATIENT):
        user_id = UserID(uuid.uuid4())
        return User(
            id=user_id.value,
            **BaseUserParams(**base_params).__dict__,
            role=role
        )