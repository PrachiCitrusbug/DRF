from rest_framework import viewsets, status, filters

# from rest_framework.decorators import action

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
    search_fields = ["username", "email"]
    queryset = user_app_service.list_users()

    def get_serializer_class(self):
        """get serializer based on action performed"""
        if self.action == "list" or self.action == "retrieve":
            return UserListViewSerializer
        elif (
            self.action == "create"
            or self.action == "update"
            or self.action == "partial_update"
        ):
            return UserCreateViewSerializer

    def list(self, request, *args, **kwargs):
        """list of users in the dataset, paginated response list and filtered response"""
        # search = request.query_params('search')
        filter_backends = [filters.SearchFilter]
        search_fields = ['username', 'email']
        for backend in filter_backends:
            self.queryset = backend().filter_queryset(request=request, queryset=self.queryset, view=self)
            
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(self.queryset, request)


        serializer = self.get_serializer_class()
        try:
            serializer = serializer(paginated_queryset, many=True)
            return CustomResponse(
                message="list data", data=serializer.data
            ).success_message()
        except Exception as e:
            return CustomResponse(
                message=e, status=status.HTTP_404_NOT_FOUND
            ).error_message()

    def retrieve(self, request, pk=None):
        """retrieve user information for the given user_id"""
        serializer = self.get_serializer_class()
        try:
            instance = self.user_app_service.get_active_user_by_id(pk)
            if instance:
                serializer = serializer(instance)
                return CustomResponse(
                    message="user object", data=serializer.data
                ).success_message()
            return CustomResponse(message="No User Found!").error_message()
        except Exception as e:
            return CustomResponse(
                message=e, status=status.HTTP_404_NOT_FOUND
            ).error_message()

    def create(self, request):
        """create user if information is valid"""
        serializer = self.get_serializer_class()
        try:
            serializer_obj = serializer(data=request.data)
            if serializer_obj.is_valid():
                serializer_obj.save()
                return CustomResponse(
                    message="User Created",
                    data=serializer_obj.data,
                    status=status.HTTP_201_CREATED,
                ).success_message()
            return CustomResponse(
                message="validation error", data=serializer_obj.errors
            ).error_message()
        except Exception as e:
            return CustomResponse(message=e).error_message()

    def update(self, request, pk=None, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        serializer = self.get_serializer_class()
        try:
            instance = self.user_app_service.get_user_by_id(pk)
            if instance:
                serializer_obj = serializer(
                    instance=instance, data=request.data, partial=partial
                )
                if serializer_obj.is_valid():
                    serializer_obj.save()
                    return CustomResponse(
                        message=f"User {instance} Updated!",
                        data=serializer_obj.data,
                        status=status.HTTP_200_OK,
                    ).success_message()
                return CustomResponse(
                    message="validation error", data=serializer_obj.errors
                ).error_message()
            return CustomResponse(message="No User Found!").error_message()
        except Exception as e:
            return CustomResponse(message=e).error_message()

    def partial_update(self, request, pk=None, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, pk, *args, **kwargs)

    def destroy(self, request, pk=None):
        """delete user, sets is_active as False"""
        try:
            instance = self.user_app_service.get_active_user_by_id(pk)
            if instance:
                instance.is_active = False
                instance.save()
                return CustomResponse(
                    message=f"User {instance} deleted!"
                ).success_message()
            return CustomResponse(
                message="No User Found!", status=status.HTTP_404_NOT_FOUND
            ).error_message()
        except Exception as e:
            return CustomResponse(message=e).error_message()

    # @action(detail=False, methods=['post'])
    # def get_username(self, request):
    #     return Response({})
