from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from rest_framework.decorators import action

from hms.application.user_management.services import UserAppService
from hms.interfaces.user_management.serializers import (
    UserListViewSerializer,
    UserCreateViewSerializer,
)


class UserViewSet(viewsets.ViewSet):
    """viewset to list, create, update, delete and retrieve users"""

    user_app_service = UserAppService()

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return UserListViewSerializer
        elif self.action == "create":
            return UserCreateViewSerializer
        
    def perform_save(self, serializer:serializers.Serializer):
        serializer.save()

    def list(self, request):
        serializer = self.get_serializer_class()
        queryset = self.user_app_service.list_users()
        serializer = serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        serializer = self.get_serializer_class()
        try:
            queryset = self.user_app_service.get_user_by_id(pk)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        if queryset:
            serializer = serializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(data="Data doesn't exist!", status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = self.get_serializer_class()
        serializer_obj = serializer(data=request.data)
        serializer_obj.is_valid(raise_exception=True)
        # print(serializer_obj.validated_data)
        self.perform_save(serializer_obj)
        return Response(serializer_obj.data)

    def update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass

    # @action(detail=False, methods=['post'])
    # def get_username(self, request):
    #     return Response({})
