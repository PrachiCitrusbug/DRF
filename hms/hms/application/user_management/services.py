import uuid
from typing import List, Optional

from django.db.models.query import QuerySet

from lib.django import custom_models
from hms.domain.user_management.models import User, BaseUserParams
from hms.domain.user_management.services import UserService


class UserAppService:
    def __init__(self) -> None:
        self.user_service = UserService()

    def get_user_by_email(self, email:str) -> Optional[QuerySet[User]]:
        """ 
        get `User` object by email
        
        Args:
            email: email to match in User object

        Returns:
            QuerySet[User] | None: The `User` object in the database or none if it DoesNotExist
        """
        try:
            return self.user_service.get_user_by_email(email)
        except User.DoesNotExist:
            return None

    def get_user_by_username(self, username:str) -> Optional[QuerySet[User]]:
        """ 
        get `User` object by username
        
        Args:
            username: username to match in User object

        Returns:
            QuerySet[User] | None: The `User` object in the database or none if it DoesNotExist
        """
        try:
            return self.user_service.get_user_by_username(username=username)
        except User.DoesNotExist:
            return None

    def list_users(self) -> Optional[QuerySet[User]]:
        """ 
        get `User` queryset
    
        Returns:
            QuerySet[User] | None: The `User` list in the database or none if it DoesNotExist
        """
        try:
            return self.user_service.get_all_users()
        except User.DoesNotExist:
            return None
        
    def list_active_users(self) -> Optional[QuerySet[User]]:
        """get `User` queryset filtered for active users"""
        try:
            return self.user_service.get_all_users().filter(is_active=True)
        except User.DoesNotExist:
            return None
        
    def list_inactive_users(self) -> Optional[QuerySet[User]]:
        """get `User` queryset filtered for inactive users"""
        try:
            return self.user_service.get_all_users().filter(is_active=False)
        except User.DoesNotExist:
            return None
        
    def list_patients(self) -> Optional[QuerySet[User]]:
        """return `User` queryset filtered for patients"""
        try:
            return self.user_service.get_all_users().filter(role=custom_models.RoleType.PATIENT)
        except User.DoesNotExist:
            return None
    
    def list_doctors(self) -> Optional[QuerySet[User]]:
        """return `User` queryset filtered for doctors"""
        try:
            return self.user_service.get_all_users().filter(role=custom_models.RoleType.DOCTOR)
        except User.DoesNotExist:
            return None
        
    def list_staffs(self) -> Optional[QuerySet[User]]:
        """return `User` queryset filtered for staffs"""
        try:
            #only return staff users not superusers
            return self.user_service.get_all_users().filter(role=custom_models.RoleType.STAFF)
        except User.DoesNotExist:
            return None
    

    def get_user_by_id(self, id: uuid.UUID) -> Optional[QuerySet[User]]:
        """ 
        get `User` object by id
        
        Args:
            id: id to match in User object

        Returns:
            QuerySet[User] | None: The `User` object in the database or none if it DoesNotExist
        """
        try:
            return self.user_service.get_user_by_id(id=id)
        except User.DoesNotExist:
            return None
        
    def get_user_by_id_list(self, id_list:List[uuid.UUID]) -> Optional[QuerySet[User]]:
        """
        get `User` queryset by list of ids

        Args:
            id_list: list of id to match in User object
        
        Returns:
            QuerySet[User] | None: The `User` object in the database or none if it DoesNotExist
        """
        try:
            return self.user_service.get_user_by_id_list(id_list)
        except User.DoesNotExist:
            return None

    def create_patient_user(self, user_obj) -> QuerySet[User]:
        """
        create patient user in the database

        Args:
            user_obj: instance of user form

        Returns:
            QuerySet[User]: created patient user
        """
        try:
            # base_params = BaseUserParams(username=user_obj.username, email=user_obj.email)
            # user = self.user_service.create_user(base_params, custom_models.RoleType.PATIENT)
            # user.set_password(user_obj.password)
            base_params = BaseUserParams(username=user_obj["username"], email=user_obj["email"])
            user = self.user_service.create_user(base_params, custom_models.RoleType.PATIENT)
            user.set_password(user_obj["password"])
            user.save()
            return user
        except Exception as e:
            return e

    def create_doctor_user(self, user_obj) -> QuerySet[User]:
        """
        create doctor user in the database

        Args:
            user_obj: instance of user form

        Returns:
            QuerySet[User]: created doctor user
        """
        try:
            # base_params = BaseUserParams(username=user_obj.username, email=user_obj.email)
            # user = self.user_service.create_user(base_params, custom_models.RoleType.DOCTOR)
            # user.set_password(user_obj.password)
            base_params = BaseUserParams(username=user_obj["username"], email=user_obj["email"])
            user = self.user_service.create_user(base_params, custom_models.RoleType.DOCTOR)
            user.set_password(user_obj["password"])
            user.save()
            return user
        except Exception as e:
            return e
