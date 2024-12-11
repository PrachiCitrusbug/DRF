import uuid
from typing import List

from django.db.models.manager import BaseManager
from django.db.models.query import QuerySet

from .models import (
    UserID,
    User,
    UserFactory,
    BaseUserParams,
    BaseUserPermissions,
    SuperUserPermission,
)
from lib.django.custom_models import RoleType


class UserService:
    """encapsulates domain specific operations for User"""

    @staticmethod
    def get_user_factory() -> UserFactory:
        """returns the `UserFactory` class, allowing access to its methods for creating `User` objects"""
        return UserFactory

    @staticmethod
    def get_user_repo() -> BaseManager[User]:
        """returns `User` objects to abstract queryset extractions"""
        # expose whole repository as a service
        # services for repo action used consistently is created separately
        return User.objects

    def get_user_by_id(self, id: UserID) -> QuerySet[User]:
        """
        returns `User` object for given `id`
        Args:
            id (UserID): id of the `User` object
        Returns:
            QuerySet[User]: `User` object
        """
        return self.get_user_repo().get(id=id)

    def get_all_users(self) -> QuerySet[User]:
        """
        get `User` object list

        Returns:
            QuerySet[User]: The `User` list in the database
        """
        return self.get_user_repo().all()

    def get_user_by_email(self, email: str) -> QuerySet[User]:
        """
        get `User` object by email

        Args:
            email: email to match in User object

        Returns:
            QuerySet[User]: The `User` object in the database
        """
        return self.get_user_repo().get(email=email)

    def get_user_by_username(self, username: str) -> QuerySet[User]:
        """
        get `User` object by username

        Args:
            username: username to match in User object

        Returns:
            QuerySet[User]: The `User` object in the database
        """
        return self.get_user_repo().get(username=username)

    def get_user_by_id_list(self, id_list: List[uuid.UUID]) -> QuerySet[User]:
        """
        get `User` queryset by list of ids

        Args:
            id_list: list of id to match in User object

        Returns:
            QuerySet[User]: The `User` object in the database
        """
        return self.get_user_repo().filter(id__in=id_list)

    def get_active_user_by_id(self, id: uuid.UUID) -> User:
        """
        returns active `User` object for given `id`
        Args:
            id (UserID): id of the `User` object
        Returns:
            User: `User` object
        """
        return self.get_user_repo().get(id=id, is_active=True)

    def create_user(
        self,
        base_params,
        role=RoleType.PATIENT,
        base_permissions={
            "is_staff": BaseUserPermissions.is_staff,
            "is_active": BaseUserPermissions.is_active,
        },
        is_superuser={"is_superuser": SuperUserPermission.is_superuser},
    ):
        """creates `User` object"""
        return self.get_user_factory().build_entity_with_id(
            base_params=base_params,
            role=role,
            base_permissions=base_permissions,
            is_superuser=is_superuser,
        )

    def update_user(
        self,
        user_id,
        base_params,
        role=RoleType.PATIENT,
        base_permissions={
            "is_staff": BaseUserPermissions.is_staff,
            "is_active": BaseUserPermissions.is_active,
        },
        is_superuser={"is_superuser": SuperUserPermission.is_superuser},
    ):
        """updates `User` object"""
        return (
            self.get_user_repo()
            .get(id=user_id)
            .update_entity(
                base_params=BaseUserParams(**base_params),
                role=role,
                base_permissions=BaseUserPermissions(**base_permissions),
                is_superuser=SuperUserPermission(**is_superuser).is_superuser
            )
        )
