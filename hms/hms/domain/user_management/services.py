import uuid
from typing import List

from django.db.models.manager import BaseManager
from django.db.models.query import QuerySet

from .models import UserID, User, UserFactory
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
        return self.get_user_repo()
    
    def get_user_by_email(self, email:str) -> QuerySet[User]:
        """ 
        get `User` object by email
        
        Args:
            email: email to match in User object

        Returns:
            QuerySet[User]: The `User` object in the database
        """
        return self.get_user_repo().get(email=email)
    
    def get_user_by_username(self, username:str) -> QuerySet[User]:
        """ 
        get `User` object by username
        
        Args:
            username: username to match in User object

        Returns:
            QuerySet[User]: The `User` object in the database
        """
        return self.get_user_repo().get(username=username)
    
    def get_user_by_id_list(self, id_list:List[uuid.UUID]) -> QuerySet[User]:
        """
        get `User` queryset by list of ids

        Args:
            id_list: list of id to match in User object
        
        Returns:
            QuerySet[User]: The `User` object in the database
        """
        return self.get_user_repo().filter(id__in=id_list)
    
    def create_user(self, base_params, role=RoleType.PATIENT):
        """updates `Appointment` object with given `base_params`"""
        return (
            self.get_user_factory().build_entity_with_id(base_params, role)
        )
