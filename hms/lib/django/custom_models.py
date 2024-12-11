# python imports
# from datetime import datetime
# from dataclasses import dataclass

# django imports
from django.db import models

class DatedModel(models.Model):
    """
    :model: includes fields that reflect when the model has been created
    or modified
    """
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class RoleType(models.TextChoices):
    """ User roles """
    PATIENT = "patient", "Patient"
    DOCTOR = "doctor", "Doctor"
    STAFF = "staff", "Staff"
    SUPERUSER = "superuser", "Superuser"

class Gender(models.TextChoices):
    """ Gender options """
    MALE = "male", "Male"
    FEMALE = "female", "Female"
    OTHER = "other", "Other"

class Specialization(models.TextChoices):
    """ Specialization options """
    ORTH = "orthopedics", "Orthopedics"
    GYNEC = "gynecology", "Gynecology"
    DERM = "dermatology", "Dermatology"
    PED = "pediatrics", "Pediatrics"
    RADIO = "radiology", "Radiology"
    GENSUR = "general", "General Surgery"
    ENT = "ent", "ENT"
    
# @dataclass(frozen=True)
# class ModelDates:
#     created_at: datetime
#     modified_at: datetime
