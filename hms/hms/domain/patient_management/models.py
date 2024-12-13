import uuid
from dataclasses import dataclass
from datetime import datetime
from dataclass_type_validator import dataclass_validate

from django.db import models
from django.core.validators import RegexValidator

from hms.domain.user_management.models import UserID
from lib.django import custom_models


@dataclass(frozen=True)
class PatientID:
    """
    This is a value object that should be used to generate and pass the PatientID to the PatientFactory
    """

    value: uuid.UUID


@dataclass_validate
@dataclass(frozen=True)
class BasePatientParams:
    """validates base patient params on type"""
    patient_name: str
    dob: datetime.date
    gender: custom_models.Gender
    contact_no: str
    address: str


class Patient(models.Model):
    """Represents a Patient's Information"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(null=False)
    patient_name = models.CharField(max_length=30)
    dob = models.DateField()
    gender = models.CharField(
        max_length=20,
        choices=custom_models.Gender.choices,
        default=custom_models.Gender.MALE,
    )
    contact_no = models.CharField(
        max_length=10,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[0-9]{10}$",
                message="Enter a valid contact number",
                code="invalid_contact_no",
            )
        ],
    )
    address = models.CharField(max_length=100)

    class Meta:
        ordering = ["patient_name"]

    def update_entity(self, base_params: BasePatientParams):
        self.patient_name = (
            base_params.patient_name if base_params.patient_name else self.patient_name
        )
        if base_params.dob:
            # TODO: add validation for checking if records are added and their dates are greater than new dob
            self.dob = base_params.dob
        else:
            self.dob = self.dob
        self.gender = base_params.gender if base_params.gender else self.gender
        self.contact_no = (
            base_params.contact_no if base_params.contact_no else self.contact_no
        )
        self.address = base_params.address if base_params.address else self.address
        


class PatientFactory:
    """Factory class for Patient Information"""

    @staticmethod
    def build_entity_with_id(user_id: UserID, base_params: BasePatientParams) -> Patient:
        patient_id = PatientID(uuid.uuid4())
        return Patient(
            id=patient_id.value,
            user_id=user_id,
            **BasePatientParams(**base_params).__dict__
        )
