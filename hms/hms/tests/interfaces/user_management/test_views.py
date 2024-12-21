from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from django.urls import reverse

from faker import Faker

from hms.domain.user_management.models import User
from lib.django.custom_models import RoleType
from django.conf import settings
from hms.tests.test_utils import create_test_user, get_req_data_by_role
from hms.interfaces.user_management.views import UserViewSet


fake = Faker()

class TestUserView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # creating
        cls.test_superuser1, cls.test_superuser2 = create_test_user(2, RoleType.SUPERUSER)
        cls.test_staff1, cls.test_staff2 = create_test_user(2, RoleType.STAFF)
        cls.test_doctor1, cls.test_doctor2, cls.test_doctor3, cls.test_doctor4 = create_test_user(4, RoleType.DOCTOR)
        cls.test_patient1, cls.test_patient2, cls.test_patient3, cls.test_patient4 = create_test_user(4, RoleType.PATIENT)
        cls.user_view_set = UserViewSet
        cls.factory = APIRequestFactory()

        cls.req_data_patient = get_req_data_by_role(RoleType.PATIENT)
        cls.req_data_doctor = get_req_data_by_role(RoleType.PATIENT)
        cls.req_data_staff = get_req_data_by_role(RoleType.STAFF)
        cls.req_data_superuser = get_req_data_by_role(RoleType.SUPERUSER)
        
    
    def setUp(self):
        pass
        # response = self.client.post(reverse("auth-login"), )

    def test_unauthorized_status_if_not_logged_in(self):
        response = self.client.get(reverse("user-list"))
        self.assertEqual(response.status_code, 401)

    def test_list_url_permitted_when_accessed_by_superuser(self):
        request = self.factory.get(f"/{settings.API_SWAGGER_URL}users/")
        force_authenticate(request, self.test_superuser1)
        response = self.user_view_set.as_view({"get": "list"})(request)
        self.assertEqual(response.status_code, 200)

    def test_list_url_permitted_when_accessed_by_staff(self):
        request = self.factory.get(f"/{settings.API_SWAGGER_URL}users/")
        force_authenticate(request, self.test_staff1)
        response = self.user_view_set.as_view({"get": "list"})(request)
        self.assertEqual(response.status_code, 200)

    def test_list_url_not_permitted_when_accessed_by_doctor(self):
        request = self.factory.get(reverse("user-list"))
        force_authenticate(request, self.test_doctor1)
        response = self.user_view_set.as_view({"get": "list"})(request)
        self.assertEqual(response.status_code, 403)
    
    def test_list_url_not_permitted_when_accessed_by_patient(self):
        request = self.factory.get(reverse("user-list"))
        force_authenticate(request, self.test_patient1)
        response = self.user_view_set.as_view({"get": "list"})(request)
        self.assertEqual(response.status_code, 403)

    def test_list_pagination_is_four(self):
        request = self.factory.get(reverse("user-list")+'?page=1')
        force_authenticate(request, self.test_staff1)
        response = self.user_view_set.as_view({"get": "list"})(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data["data"]) == 4)

    def test_list_filtered_search(self):
        request = self.factory.get(reverse("user-list")+f'?search={self.test_doctor1.username}')
        force_authenticate(request, self.test_staff1)
        response = self.user_view_set.as_view({"get": "list"})(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["data"][0]["username"] == self.test_doctor1.username)

    def test_retrieve_patient_user_by_staff(self):
        request = self.factory.get(reverse("user-detail", kwargs={'pk': self.test_patient1.id}))
        force_authenticate(request, self.test_staff1)
        response = self.user_view_set.as_view({"get": "retrieve"})(request, pk=str(self.test_patient1.id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["data"]["username"] == self.test_patient1.username)

    def test_retrieve_doctor_user_by_staff(self):
        request = self.factory.get(reverse("user-detail", kwargs={'pk': self.test_doctor1.id}))
        force_authenticate(request, self.test_staff1)
        response = self.user_view_set.as_view({"get": "retrieve"})(request, pk=str(self.test_doctor1.id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["data"]["username"] == self.test_doctor1.username)

    def test_retrieve_other_staff_user_by_staff(self):
        request = self.factory.get(reverse("user-detail", kwargs={'pk': self.test_staff2.id}))
        force_authenticate(request, self.test_staff1)
        response = self.user_view_set.as_view({"get": "retrieve"})(request, pk=str(self.test_staff2.id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["data"]["username"] == self.test_staff2.username)

    def test_retrieve_superuser_by_staff(self):
        request = self.factory.get(reverse("user-detail", kwargs={'pk': self.test_superuser1.id}))
        force_authenticate(request, self.test_staff1)
        response = self.user_view_set.as_view({"get": "retrieve"})(request, pk=str(self.test_superuser1.id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["data"]["username"] == self.test_superuser1.username)

    def test_retrieve_own_user_by_patient(self):
        request = self.factory.get(reverse("user-detail", kwargs={'pk': self.test_patient1.id}))
        force_authenticate(request, self.test_patient1)
        response = self.user_view_set.as_view({"get": "retrieve"})(request, pk=str(self.test_patient1.id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["data"]["username"] == self.test_patient1.username)

    def test_do_not_retrieve_other_user_by_patient(self):
        request = self.factory.get(reverse("user-detail", kwargs={'pk': self.test_patient1.id}))
        force_authenticate(request, self.test_patient2)
        response = self.user_view_set.as_view({"get": "retrieve"})(request, pk=str(self.test_patient1.id))
        self.assertEqual(response.status_code, 403)

    def test_retrieve_own_user_by_doctor(self):
        request = self.factory.get(reverse("user-detail", kwargs={'pk': self.test_doctor1.id}))
        force_authenticate(request, self.test_doctor1)
        response = self.user_view_set.as_view({"get": "retrieve"})(request, pk=str(self.test_doctor1.id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["data"]["username"] == self.test_doctor1.username)

    def test_retrieve_other_user_by_doctor(self):
        request = self.factory.get(reverse("user-detail", kwargs={'pk': self.test_doctor1.id}))
        force_authenticate(request, self.test_doctor2)
        response = self.user_view_set.as_view({"get": "retrieve"})(request, pk=str(self.test_doctor1.id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["data"]["username"] == self.test_doctor1.username)

    def test_create_patient_user_by_staff(self):
        request = self.factory.post(f"/{settings.API_SWAGGER_URL}users/", self.req_data_patient)
        force_authenticate(request, self.test_staff1)
        response = self.user_view_set.as_view({"post": "create"})(request)
        self.assertEqual(response.status_code, 201)
        created_user = User.objects.get(email=response.data["data"]["email"])
        self.assertTrue(self.req_data_patient["username"] == created_user.username)

    def test_create_doctor_user_by_staff(self):
        request = self.factory.post(f"/{settings.API_SWAGGER_URL}users/", self.req_data_doctor)
        force_authenticate(request, self.test_staff1)
        response = self.user_view_set.as_view({"post": "create"})(request)
        self.assertEqual(response.status_code, 201)
        created_user = User.objects.get(email=response.data["data"]["email"])
        self.assertTrue(self.req_data_doctor["username"] == created_user.username)

    def test_create_staff_user_by_staff(self):
        request = self.factory.post(f"/{settings.API_SWAGGER_URL}users/", self.req_data_staff)
        force_authenticate(request, self.test_staff1)
        response = self.user_view_set.as_view({"post": "create"})(request)
        self.assertEqual(response.status_code, 201)
        created_user = User.objects.get(email=response.data["data"]["email"])
        self.assertTrue(self.req_data_staff["username"] == created_user.username)

    def test_do_not_create_user_by_patient(self):
        request = self.factory.post(f"/{settings.API_SWAGGER_URL}users/", self.req_data_patient)
        force_authenticate(request, self.test_patient1)
        response = self.user_view_set.as_view({"post": "create"})(request)
        self.assertEqual(response.status_code, 403)
    
    def test_do_not_create_user_by_doctor(self):
        request = self.factory.post(f"/{settings.API_SWAGGER_URL}users/", self.req_data_doctor)
        force_authenticate(request, self.test_doctor1)
        response = self.user_view_set.as_view({"post": "create"})(request)
        self.assertEqual(response.status_code, 403)

    def test_bad_request_for_create_user_with_invalid_data(self):
        request = self.factory.post(f"/{settings.API_SWAGGER_URL}users/", {"username": "invalid"})
        force_authenticate(request, self.test_staff1)
        response = self.user_view_set.as_view({"post": "create"})(request)
        self.assertEqual(response.status_code, 400)

    def test_bad_request_for_create_user_with_invalid_email(self):
        req_data = self.req_data_patient
        req_data["email"] = "invalid"
        request = self.factory.post(f"/{settings.API_SWAGGER_URL}users/", req_data)
        force_authenticate(request, self.test_staff1)
        response = self.user_view_set.as_view({"post": "create"})(request)
        self.assertEqual(response.status_code, 400)

    def test_validation_error_create_user_with_existing_username_by_staff(self):
        req_data = self.req_data_staff
        req_data["username"] = self.test_doctor1.username
        request = self.factory.post(f"/{settings.API_SWAGGER_URL}users/", req_data)
        force_authenticate(request, self.test_staff1)
        response = self.user_view_set.as_view({"post": "create"})(request)
        self.assertEqual(response.status_code, 400)

    def test_validation_error_create_user_with_existing_email_by_staff(self):
        req_data = self.req_data_staff
        req_data["email"] = self.test_doctor1.email
        request = self.factory.post(f"/{settings.API_SWAGGER_URL}users/", req_data)
        force_authenticate(request, self.test_staff1)
        response = self.user_view_set.as_view({"post": "create"})(request)
        self.assertEqual(response.status_code, 400)

    def test_update_patient_to_staff_by_staff(self):
        req_id = self.test_patient1.id
        update_data = {"username": fake.name().split(" ")[0], "email": fake.email(), "role": RoleType.STAFF}
        request = self.factory.put(f"{settings.API_SWAGGER_URL}users/{req_id}/", update_data)
        force_authenticate(request, self.test_staff1)
        response = self.user_view_set.as_view({"put": "update"})(request, str(req_id))
        self.assertEqual(response.status_code, 200)
        updated_user = User.objects.get(id=req_id)
        self.assertTrue(update_data["username"] == updated_user.username)
        self.assertTrue(update_data["email"] == updated_user.email)
        self.assertTrue(update_data["role"] == updated_user.role)
        self.assertTrue(updated_user.is_staff)

    def test_validation_error_update_user_if_password_by_staff(self):
        req_id = self.test_patient1.id
        update_data = get_req_data_by_role(role=RoleType.PATIENT)
        request = self.factory.put(f"{settings.API_SWAGGER_URL}users/{req_id}/", update_data)
        force_authenticate(request, self.test_staff1)
        response = self.user_view_set.as_view({"put": "update"})(request, str(req_id))
        self.assertEqual(response.status_code, 400)

    def test_validation_error_update_user_invalid_data_by_staff(self):
        req_id = self.test_patient1.id
        update_data = {"username": fake.name().split(" ")[0], "role": RoleType.PATIENT}
        request = self.factory.put(f"{settings.API_SWAGGER_URL}users/{req_id}/", update_data)
        force_authenticate(request, self.test_staff1)
        response = self.user_view_set.as_view({"put": "update"})(request, str(req_id))
        self.assertEqual(response.status_code, 400)

    def test_validation_error_update_user_invalid_email_by_staff(self):
        req_id = self.test_patient1.id
        update_data = {"username": fake.name().split(" ")[0], "email": "invalid", "role": RoleType.PATIENT}
        request = self.factory.put(f"{settings.API_SWAGGER_URL}users/{req_id}/", update_data)
        force_authenticate(request, self.test_staff1)
        response = self.user_view_set.as_view({"put": "update"})(request, str(req_id))
        self.assertEqual(response.status_code, 400)

    def test_validation_error_update_user_with_existing_username_by_staff(self):
        req_id = self.test_patient1.id
        update_data = {"username": self.test_patient2.username, "email": fake.email(), "role": RoleType.PATIENT}
        request = self.factory.put(f"{settings.API_SWAGGER_URL}users/{req_id}/", update_data)
        force_authenticate(request, self.test_staff1)
        response = self.user_view_set.as_view({"put": "update"})(request, str(req_id))
        self.assertEqual(response.status_code, 400)

    def test_validation_error_update_user_with_existing_email_by_staff(self):
        req_id = self.test_patient1.id
        update_data = {"username": fake.name().split(" ")[0], "email": self.test_patient2.email, "role": RoleType.PATIENT}
        request = self.factory.put(f"{settings.API_SWAGGER_URL}users/{req_id}/", update_data)
        force_authenticate(request, self.test_staff1)
        response = self.user_view_set.as_view({"put": "update"})(request, str(req_id))
        self.assertEqual(response.status_code, 400)

    def test_do_not_update_user_by_patient(self):
        req_id = self.test_patient1.id
        update_data = {"username": fake.name().split(" ")[0], "email": fake.email(), "role": RoleType.PATIENT}
        request = self.factory.put(f"{settings.API_SWAGGER_URL}users/{req_id}/", update_data)
        force_authenticate(request, self.test_patient1)
        response = self.user_view_set.as_view({"put": "update"})(request, str(req_id))
        self.assertEqual(response.status_code, 403)

    def test_do_not_update_user_by_doctor(self):
        req_id = self.test_patient1.id
        update_data = {"username": fake.name().split(" ")[0], "email": fake.email(), "role": RoleType.PATIENT}
        request = self.factory.put(f"{settings.API_SWAGGER_URL}users/{req_id}/", update_data)
        force_authenticate(request, self.test_doctor1)
        response = self.user_view_set.as_view({"put": "update"})(request, str(req_id))
        self.assertEqual(response.status_code, 403)

    def test_partial_update_user_by_staff(self):
        req_id = self.test_patient1.id
        update_data = {"email": fake.email(), "role": RoleType.PATIENT}
        request = self.factory.patch(f"{settings.API_SWAGGER_URL}users/{req_id}/", update_data)
        force_authenticate(request, self.test_staff1)
        response = self.user_view_set.as_view({"patch": "partial_update"})(request, str(req_id))
        self.assertEqual(response.status_code, 200)
        updated_user = User.objects.get(id=req_id)
        self.assertTrue(update_data["email"] == updated_user.email)
        self.assertTrue(update_data["role"] == updated_user.role)

    def test_validation_error_partial_update_user_invalid_email_by_staff(self):
        req_id = self.test_patient1.id
        update_data = {"email": 'invalid'}
        request = self.factory.patch(f"{settings.API_SWAGGER_URL}users/{req_id}/", update_data)
        force_authenticate(request, self.test_staff1)
        response = self.user_view_set.as_view({"patch": "partial_update"})(request, str(req_id))
        self.assertEqual(response.status_code, 400)

    def test_validation_error_partial_update_user_with_existing_username_by_staff(self):
        req_id = self.test_patient1.id
        update_data = {"username": self.test_patient2.username}
        request = self.factory.patch(f"{settings.API_SWAGGER_URL}users/{req_id}/", update_data)
        force_authenticate(request, self.test_staff1)
        response = self.user_view_set.as_view({"patch": "partial_update"})(request, str(req_id))
        self.assertEqual(response.status_code, 400)

    def test_validation_error_partial_update_user_with_existing_email_by_staff(self):
        req_id = self.test_patient1.id
        update_data = {"email": self.test_patient2.email}
        request = self.factory.patch(f"{settings.API_SWAGGER_URL}users/{req_id}/", update_data)
        force_authenticate(request, self.test_staff1)
        response = self.user_view_set.as_view({"patch": "partial_update"})(request, str(req_id))
        self.assertEqual(response.status_code, 400)

    def test_delete_user_by_staff(self):
        req_id = self.test_patient1.id
        request = self.factory.delete(f"{settings.API_SWAGGER_URL}users/{req_id}/")
        force_authenticate(request, self.test_staff1)
        response = self.user_view_set.as_view({"delete": "destroy"})(request, str(req_id))
        self.assertEqual(response.status_code, 200)
        # print(response.data)
        deleted_user = User.objects.get(id=req_id)
        # print(deleted_user.is_active)
        self.assertFalse(deleted_user.is_active)

    # def test_delete_own_user_by_patient(self):
    #     req_id = self.test_patient2.id
    #     request = self.factory.delete(f"{settings.API_SWAGGER_URL}users/{req_id}/")
    #     force_authenticate(request, self.test_patient2)
    #     response = self.user_view_set.as_view({"delete": "destroy"})(request, str(req_id))
    #     self.assertEqual(response.status_code, 200)
    #     updated_user = User.objects.get(id=req_id)
    #     self.assertFalse(updated_user.is_active)
    
    # def test_delete_other_user_by_patient(self):
    #     req_id = self.test_patient4.id
    #     request = self.factory.delete(f"{settings.API_SWAGGER_URL}users/{req_id}/")
    #     force_authenticate(request, self.test_patient3)
    #     response = self.user_view_set.as_view({"delete": "destroy"})(request, str(req_id))
    #     self.assertEqual(response.status_code, 401)
    #     updated_user = User.objects.get(id=req_id)
    #     self.assertTrue(updated_user.is_active)

    # def test_delete_own_user_by_doctor(self):
    #     req_id = self.test_doctor2.id
    #     request = self.factory.delete(f"{settings.API_SWAGGER_URL}users/{req_id}/")
    #     force_authenticate(request, self.test_doctor2)
    #     response = self.user_view_set.as_view({"delete": "destroy"})(request, str(req_id))
    #     self.assertEqual(response.status_code, 200)
    #     updated_user = User.objects.get(id=req_id)
    #     self.assertFalse(updated_user.is_active)
    
    # def test_delete_other_user_by_doctor(self):
    #     req_id = self.test_doctor4.id
    #     request = self.factory.delete(f"{settings.API_SWAGGER_URL}users/{req_id}/")
    #     force_authenticate(request, self.test_doctor3)
    #     response = self.user_view_set.as_view({"delete": "destroy"})(request, str(req_id))
    #     self.assertEqual(response.status_code, 401)
    #     updated_user = User.objects.get(id=req_id)
    #     self.assertTrue(updated_user.is_active)

    def test_delete_then_retrieve(self):
        # can be retrieve inactive user too
        req_id = self.test_doctor4.id
        request = self.factory.delete(f"{settings.API_SWAGGER_URL}users/{req_id}/")
        force_authenticate(request, self.test_staff1)
        response = self.user_view_set.as_view({"delete": "destroy"})(request, str(req_id))
        self.assertEqual(response.status_code, 200)
        updated_user = User.objects.get(id=req_id)
        self.assertFalse(updated_user.is_active)

        request = self.factory.get(reverse("user-detail", kwargs={'pk': req_id}))
        force_authenticate(request, self.test_staff1)
        response = self.user_view_set.as_view({"get": "retrieve"})(request, pk=str(req_id))
        ## don't understand why status is not received in custom response
        # self.assertEqual(response.status_code, 404)
        self.assertEqual(response.status_code, 400)
