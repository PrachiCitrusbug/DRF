import uuid

from django.contrib.auth.mixins import UserPassesTestMixin

from rest_framework.permissions import BasePermission

from lib.django.custom_models import RoleType



class UserAuthenticatedTestMixin(UserPassesTestMixin):
    """ test mixin class to check requested user is authenticated """
    def test_func(self) -> bool | None:
        return self.request.user.is_authenticated
    
class NotPatientTestMixin(UserPassesTestMixin):
    """ test mixin class to check requested user's role is not patient """
    def test_func(self) -> bool | None:
        return self.request.user.is_authenticated and self.request.user.role != RoleType.PATIENT
    
class NotDoctorTestMixin(UserPassesTestMixin):
    """ test mixin class to check requested user's role is not doctor """
    def test_func(self) -> bool | None:
        return self.request.user.is_authenticated and self.request.user.role != RoleType.DOCTOR

class IsNotAuthenticated(BasePermission):
    """
    Custom permission to restrict access for authenticated users.
    """
    message = 'Authenticated users are not allowed.'

    def has_permission(self, request, view):
        return not request.user.is_authenticated
    
class PatientNotAllowed(BasePermission):
    """Custom permission to restrict patient user access"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role != RoleType.PATIENT
    
class DoctorNotAllowed(BasePermission):
    """Custom permission to restrict doctor user access"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role != RoleType.DOCTOR
    
class OwnDataAccess(BasePermission):
    """only allow user to access their own data"""
    def has_permission(self, request, view):
        # print("VIEW", view.kwargs.get("pk"))
        pk = uuid.UUID(view.kwargs.get("pk"))
        return request.user.id == pk