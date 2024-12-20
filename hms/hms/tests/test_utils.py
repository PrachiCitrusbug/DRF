from faker import Faker

from hms.domain.user_management.models import User
from lib.django.custom_models import RoleType

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
        users.append(User.objects.create_superuser(username=fake.name(), email=fake.email(), password="practice123"))
    return users