import uuid

from django.db.models.manager import BaseManager
from django.db.models.query import QuerySet

from .models import PatientID, Patient, PatientFactory

class PatientService:
    """encapsulates domain specific operations for Patient"""

    @staticmethod
    def get_patient_factory() -> PatientFactory:
        """returns the `PatientFactory` class, allowing access to its methods for creating `Patient` objects"""
        return PatientFactory
    
    @staticmethod
    def get_patient_repo() -> BaseManager[Patient]:
        """returns `Patient` objects to abstract queryset extractions"""
        # expose whole repository as a service
        # services for repo action used consistently is created separately
        return Patient.objects


    def get_patient_by_id(self, id: PatientID) -> QuerySet[Patient]:
        """
        returns `Patient` object for given `id`
        Args:
            id (PatientID): id of the `Patient` object
        Returns:
            QuerySet[Patient]: `Patient` object
        """
        return self.get_patient_repo().get(id=id)
    
    def get_patient_by_user_id(self, id: uuid.UUID) -> QuerySet[Patient]:
        """
        returns `Patient` object for given `user id`
        Args:
            id (UserID): id of the `User` object
        Returns:
            QuerySet[Patient]: `Patient` object
        """
        return self.get_patient_repo().get(user_id=id)

    def get_patient_list(self) -> QuerySet[Patient]:
        """returns `Patient` list """
        return self.get_patient_repo().all()
    
    def create_patient_info(self, user_id:uuid.UUID, patient:dict) -> Patient:
        """creates patient information for given user id"""
        return self.get_patient_factory().build_entity_with_id(user_id=user_id, base_params=patient)