import uuid
from typing import Optional

from django.db.models.query import QuerySet

from hms.application.user_management.services import UserAppService
from hms.domain.patient_management.models import Patient
from hms.domain.patient_management.services import PatientService

class PatientAppService:
    def __init__(self):
        self.patient_service = PatientService()
        self.user_service = UserAppService()

    def get_patient_by_id(self, id:uuid.UUID) -> Patient:
        """ get patient by id stored in Patient model """
        return self.patient_service.get_patient_by_id(id=id)
    
    def get_patient_by_username(self, username:str) -> Optional[Patient]:
        """ get patient user by username stored in User model """
        #1. get userid using username
        user_id = self.user_service.get_user_by_username(username=username).id
        #2. search for user_id in patient model
        try:
            patient = self.patient_service.get_patient_by_user_id(user_id)
            return patient
        except Patient.DoesNotExist:
            return None
        
    def create_patient_info(self, user_id:uuid.UUID, patient) -> Patient:
        """create patient information queryset"""
        patient = self.patient_service.create_patient_info(user_id, patient.__dict__)
        patient.save()
        return patient
    
    def get_patient_username(self, patient_id: uuid.UUID) -> str:
        """get patient username using patient_id"""
        user_id = self.patient_service.get_patient_by_id(patient_id).user_id
        username = self.user_service.get_user_by_id(user_id).username
        return username
    
    def list_patients(self) -> QuerySet[Patient]:
        """ list all patients """
        return self.patient_service.get_patient_list()
            