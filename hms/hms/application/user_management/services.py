import uuid
from typing import List, Optional

from rest_framework_simplejwt.tokens import RefreshToken

from django.db.models.query import QuerySet
from django.urls import reverse

from lib.django import custom_models
from lib.django.custom_exceptions import OTPExpireException
from hms.domain.user_management.models import User, UserOTP
from hms.domain.user_management.services import UserService


class UserAppService:
    def __init__(self) -> None:
        self.user_service = UserService()

    def get_user_by_email(self, email: str) -> Optional[QuerySet[User]]:
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

    def get_user_by_username(self, username: str) -> Optional[QuerySet[User]]:
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
            return self.user_service.get_all_users().order_by("date_joined")
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
            return self.user_service.get_all_users().filter(
                role=custom_models.RoleType.PATIENT
            )
        except User.DoesNotExist:
            return None

    def list_doctors(self) -> Optional[QuerySet[User]]:
        """return `User` queryset filtered for doctors"""
        try:
            return self.user_service.get_all_users().filter(
                role=custom_models.RoleType.DOCTOR
            )
        except User.DoesNotExist:
            return None

    def list_staffs(self) -> Optional[QuerySet[User]]:
        """return `User` queryset filtered for staffs"""
        try:
            # only return staff users not superusers
            return self.user_service.get_all_users().filter(
                role=custom_models.RoleType.STAFF
            )
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

    def get_user_by_id_list(self, id_list: List[uuid.UUID]) -> Optional[QuerySet[User]]:
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

    def get_active_user_by_id(self, id: uuid.UUID) -> Optional[User]:
        """
        get active `User` object by id

        Args:
            id: id to match in User object

        Returns:
            QuerySet[User] | None: The `User` object in the database or none if it DoesNotExist
        """
        try:
            return self.user_service.get_active_user_by_id(id)
        except User.DoesNotExist:
            return None

    def create_user(self, user_obj: dict) -> User:
        """
        create user based on role

        Args:
            user_obj: dict with user model attributes as keys

        Returns:
            User: created user object
        """
        try:
            # base_params = BaseUserParams(username=user_obj.username, email=user_obj.email)
            # user = self.user_service.create_user(base_params, custom_models.RoleType.PATIENT)
            # user.set_password(user_obj.password)
            base_params = {
                "username": user_obj.get("username"),
                "email": user_obj.get("email"),
            }
            role = user_obj.get("role")
            if role == custom_models.RoleType.PATIENT or role == custom_models.RoleType.DOCTOR:
                user = self.user_service.create_user(
                    base_params=base_params, role=role
                )
            elif role == custom_models.RoleType.STAFF:
                user = self.user_service.create_user(
                    base_params=base_params,
                    role=custom_models.RoleType.STAFF,
                    base_permissions={"is_staff": True},
                )
            elif role == custom_models.RoleType.SUPERUSER:
                user = self.user_service.create_user(
                    base_params=base_params,
                    role=custom_models.RoleType.SUPERUSER,
                    base_permissions={"is_staff": True},
                    is_superuser={"is_superuser": True}
                )
            else:
                user = self.user_service.create_user(
                    base_params=base_params,
                    role=custom_models.RoleType.PATIENT,
                )
            user.set_password(user_obj.get("password"))
            user.save()
            return user
        except Exception as e:
            raise Exception(f"At create_user: {e}. user_obj dict must contain username, email, password and role key values.")


    def update_user(self, user_obj: User) -> QuerySet[User]:
        """
        update user based on role

        Args:
            user_obj: instance of user form

        Returns:
            User: updated user instance

        """
        try:
            user_id = user_obj.id
            base_params = {"username": user_obj.username, "email": user_obj.email}
            role = user_obj.role if user_obj.role else custom_models.RoleType.PATIENT
            base_permissions = {"is_staff": True} if role == custom_models.RoleType.STAFF or role == custom_models.RoleType.SUPERUSER else None
            is_superuser = {"is_superuser": True} if role == custom_models.RoleType.SUPERUSER else None
            # TODO : Update this code to call update_user only one time. - DONE
            return self.user_service.update_user(
                    user_id=user_id,
                    base_params=base_params,
                    role=role,
                    base_permissions=base_permissions,
                    is_superuser=is_superuser
                )  
        except Exception as e:
            raise Exception(f"At update_user: {e}. user_obj is an instance of User object with updated values.")
    
    def get_user_token(self, user:User) -> dict:
        """
        generate access and refresh token for the user 

        Args:
            user: authenticated user

        Returns:
            dict: containing information about user and token
        """
        try:
            token = RefreshToken.for_user(user)
            token["email"] = user.email
            data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "access token": str(token.access_token),
                "refresh token": str(token),
            }
            return data
        except Exception as e:
            raise Exception(f"At get_user_token: {e}")
    
    
    def forgot_password(self, user:User) -> dict:
        try:
            #get otp -> delete if exists
            otp_obj = self.user_service.get_otp_by_user_id(user_id=user.id)
            if otp_obj:
                otp_obj.delete()
            otp = self.user_service.create_otp(user=user)
            otp.save()
            response_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'otp': otp.otp,
                'verify': reverse('pwd-verify-otp', kwargs={'pk': user.id}),
            }
            return response_data
        except Exception as e:
            raise Exception(f"At forgot_password: {e}")
    
    def verify_otp(self, otp:int, user_id:uuid.UUID) -> UserOTP:
        try:
            otp_obj = self.user_service.get_otp_by_user_id(user_id=user_id)
            if otp_obj.otp == otp:
                #check for otp expiration
                if not otp_obj.is_otp_expired():
                    return otp_obj
                raise OTPExpireException("Your OTP has expired")
        except OTPExpireException:
            otp_obj.delete
            raise OTPExpireException
        except Exception as e:
            raise Exception(f"At verify_otp: {e}")
    
    def set_new_password(self, user_id: uuid.UUID, new_password:str) -> bool:
        try:
            user = self.user_service.get_user_by_id(id=user_id)
            user.set_password(new_password)
            user.save()
            return True
        except Exception as e:
            raise Exception(f"At set_new_password: {e}")
        
    def reset_password(self, otp_token, user_id:uuid.UUID, new_password) -> bool:
        try:
            otp_obj = self.user_service.get_otp_by_user_id(user_id=user_id)
            if otp_obj.otp_token == otp_token:
                otp_obj.delete()
                return self.set_new_password(user_id=user_id, new_password=new_password)
            return False
        except Exception as e:
            raise Exception(f"At reset_password: {e}")