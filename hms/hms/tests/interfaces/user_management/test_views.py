from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from django.urls import reverse

from hms.domain.user_management.models import User
from lib.django.custom_models import RoleType
from django.conf import settings
from hms.tests.test_utils import create_test_user
from hms.interfaces.user_management.views import UserViewSet




class TestUserView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # creating
        cls.test_staff1 = create_test_user(1, RoleType.STAFF)[0]
        # print(cls.test_staff1)
        cls.user_view_set = UserViewSet
        cls.factory = APIRequestFactory()
        
    
    def setUp(self):
        pass
        # response = self.client.post(reverse("auth-login"), )

    def test_unauthorized_status_if_not_logged_in(self):
        response = self.client.get(reverse("user-list"))
        self.assertEqual(401, response.status_code)

    def test_list_url_exists_at_desired_location(self):
        request = self.factory.get(f"/{settings.API_SWAGGER_URL}users/")
        force_authenticate(request, self.test_staff1)
        response = self.user_view_set.as_view({"get": "list"})(request)
        self.assertEqual(200, response.status_code)

    def test_list_url_accessible_by_name(self):
        response = self.client.get(reverse("user-list"))
        print(response)

    def test_pagination_is_seven(self):
        response = self.client.get(reverse("user-list")+'?page=1')

    def test_list_all_users(self):
        pass

    #tests with patient, doctor, staff access
    
# class TestPatientUserView(TestCase):
#     pass

# class TestUnauthorizedUserView(TestCase):
   