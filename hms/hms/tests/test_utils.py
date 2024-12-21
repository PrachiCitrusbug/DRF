from faker import Faker
import jwt

from hms.domain.user_management.models import User
from lib.django.custom_models import RoleType
from django.conf import settings

fake = Faker()

def create_test_user(num, role):
    users = []
    if role == RoleType.PATIENT or role == RoleType.DOCTOR:
        for i in range(num):
            users.append(User.objects.create_user(username=fake.name(), email=fake.email(), password="practice123", role=role))
    elif role == RoleType.STAFF:
        for i in range(num):
            users.append(User.objects.create_staff(username=fake.name(), email=fake.email(), password="practice123", role=role))
    elif role == RoleType.SUPERUSER:
        for i in range(num):
            users.append(User.objects.create_superuser(username=fake.name(), email=fake.email(), password="practice123"))
    return users

def get_req_data_by_role(role:RoleType):
    return {"username": fake.name().split(" ")[0], "email": fake.email(), "password": "practice123", "role": role}

def decode_jwt_token(self, token):
    secret = settings.SIMPLE_JWT["SIGNING_KEY"]
    decoded = jwt.decode(token, secret, algorithms=["HS256"])
    return decoded