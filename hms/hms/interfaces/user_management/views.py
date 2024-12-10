from rest_framework import viewsets, status, serializers, filters
# from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

from hms.application.user_management.services import UserAppService
from hms.interfaces.user_management.serializers import (
    UserListViewSerializer,
    UserCreateViewSerializer,
)
from lib.django.custom_response import CustomResponse

class UserViewSet(viewsets.GenericViewSet):
    """viewset to list, create, update, delete and retrieve users"""

    user_app_service = UserAppService()
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return UserListViewSerializer
        elif self.action == "create" or self.action == "update":
            return UserCreateViewSerializer
        
    def get_queryset(self):
        return self.user_app_service.list_users()
        
    def perform_save(self, serializer:serializers.Serializer):
        serializer.save()

    def list(self, request):
        serializer = self.get_serializer_class()
        queryset = self.get_queryset()
        serializer = serializer(queryset, many=True)
        # print(self.get_paginated_response(serializer.data))
        print(self.paginator.__dict__)
        return CustomResponse(message="list data", data=serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        serializer = self.get_serializer_class()
        try:
            instance = self.user_app_service.get_active_user_by_id(pk)
            if instance:
                serializer = serializer(instance)
                return CustomResponse(message="user object", data=serializer.data, status=status.HTTP_200_OK)
            return CustomResponse(message="Data doesn't exist!", status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return CustomResponse(message=e, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return CustomResponse(message=e, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = self.get_serializer_class()
        serializer_obj = serializer(data=request.data)
        serializer_obj.is_valid(raise_exception=True)
        # print(serializer_obj.validated_data)
        self.perform_save(serializer_obj)
        return CustomResponse(message="User Created", data=serializer_obj.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        serializer = self.get_serializer_class()
        instance = self.user_app_service.get_user_by_id(pk)
        if instance:
            serializer_obj = serializer(instance=instance, data=request.data)
            serializer_obj.is_valid(raise_exception=True)
        return CustomResponse(message=f"User {instance} Updated!", data=serializer_obj.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        instance = self.user_app_service.get_active_user_by_id(pk)
        if instance:
            instance.is_active = False
            instance.save()
        return CustomResponse(message=f"User {instance} deleted!", status=status.HTTP_200_OK)

    # @action(detail=False, methods=['post'])
    # def get_username(self, request):
    #     return Response({})
