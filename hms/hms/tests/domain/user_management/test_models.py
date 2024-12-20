import uuid
import datetime

from rest_framework.test import APITestCase

from django.db.utils import IntegrityError

from psycopg2.errors import UniqueViolation

from hms.domain.user_management.models import User
from lib.django.custom_models import RoleType
from django.conf import settings

class TestUserModel(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.id = uuid.uuid4()
        cls.instance_kwargs = {"id": cls.id, "username": "patient", "email":"patient@gmail.com", "password": "practice123", "role": RoleType.PATIENT}
        cls.user = User.objects.create(**cls.instance_kwargs)
        
    def setUp(self):
    
        pass

    def test_unique_id_enforced(self):
        same_id_data = {"id": self.id, "username": "patient2", "email":"patient2@gmail.com", "password": "practice123", "role": RoleType.PATIENT}
        with self.assertRaises((IntegrityError, UniqueViolation)):
            User.objects.create(**same_id_data)
    
    def test_unique_username_enforced(self):
        same_username_data = {"username": "patient", "email":"patient2@gmail.com", "password": "practice123", "role": RoleType.PATIENT}
        with self.assertRaises((IntegrityError, UniqueViolation)):
            User.objects.create(**same_username_data)

    def test_unique_email_enforced(self):
        same_email_data = {"username": "patient2", "email":"patient@gmail.com", "password": "practice123", "role": RoleType.PATIENT}
        with self.assertRaises((IntegrityError, UniqueViolation)):
            User.objects.create(**same_email_data)
    
    def test_default_role_value_as_patient(self):
        no_role_data = {"username": "patient2", "email":"patient2@gmail.com", "password": "practice123"}
        user = User.objects.create(**no_role_data)
        self.assertEqual(RoleType.PATIENT, user.role)
    
    # same for booleans too
    def test_added_date_joined_automatically(self):
        self.assertTrue(type(self.user.date_joined), datetime)

    def test_str(self):
        self.assertEqual(self.instance_kwargs["username"], str(self.user))

    def test_absolute_url(self):
        self.assertEqual(f"/{settings.API_SWAGGER_URL}users/{self.user.pk}/", self.user.get_absolute_url())
    