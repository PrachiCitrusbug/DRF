from django.contrib.auth.mixins import UserPassesTestMixin

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
