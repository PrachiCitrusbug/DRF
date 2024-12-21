from rest_framework.test import APITestCase, APIRequestFactory

from hms.domain.user_management.models import User
from lib.django.custom_models import RoleType
from django.conf import settings
from hms.tests.test_utils import create_test_user, get_req_data_by_role
from hms.interfaces.auth.views import AuthenticateUserView

class TestAuthentication(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # creating
        cls.test_superuser1, cls.test_superuser2 = create_test_user(2, RoleType.SUPERUSER)
        cls.test_staff1, cls.test_staff2 = create_test_user(2, RoleType.STAFF)
        cls.test_doctor1, cls.test_doctor2, cls.test_doctor3, cls.test_doctor4 = create_test_user(4, RoleType.DOCTOR)
        cls.test_patient1, cls.test_patient2, cls.test_patient3, cls.test_patient4 = create_test_user(4, RoleType.PATIENT)
        cls.auth_view_set = AuthenticateUserView
        cls.factory = APIRequestFactory()

        cls.req_data_patient = get_req_data_by_role(RoleType.PATIENT)
        cls.req_data_doctor = get_req_data_by_role(RoleType.PATIENT)
        cls.req_data_staff = get_req_data_by_role(RoleType.STAFF)
        cls.req_data_superuser = get_req_data_by_role(RoleType.SUPERUSER)

    def test_login(self):
        req_data = self.test_patient1.__dict__
        response = self.client.get(f"{settings.API_SWAGGER_URL}auth/login/", req_data)
        

