from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout

from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.exceptions import TokenError


from .serializers import AuthSerializer
from ..user_management.serializers import UserCreateViewSerializer
from hms.application.user_management.services import UserAppService
from lib.django.custom_response import CustomResponse
from hms.domain.user_management.models import User


class AuthenticateUserView(viewsets.ViewSet):
    """viewset to login, signup and logout user"""

    user_app_service = UserAppService()

    def get_serializer_class(self):
        if self.action == "login":
            return AuthSerializer
        elif self.action == "register":
            return UserCreateViewSerializer

    @action(methods=["post"], detail=False, url_name="login")
    def login(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        try:
            if request.user.is_authenticated:
                return CustomResponse(
                    message="User already logged in, log out first!",
                    status=status.HTTP_400_BAD_REQUEST,
                ).error_message()
            serializer = serializer(data=request.data)
            if serializer.is_valid():
                email = serializer.data.get("email", None)
                password = serializer.data.get("password", None)
                user = authenticate(email=email, password=password)
                # TODO : Add condition to raise error if user not found.
                response_data = self.user_app_service.get_user_token(user)
                return CustomResponse(
                    message="Logged In", data=response_data
                ).success_message()
            return CustomResponse(
                message="validation error", data=serializer.errors
            ).error_message()
        except Exception as e:
            return CustomResponse(
                message=e, status=status.HTTP_404_NOT_FOUND
            ).error_message()

    @action(methods=["post"], detail=False, url_name="register")
    def register(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        try:
            serializer = serializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                response_data = self.user_app_service.get_user_token(user)
                return CustomResponse(
                    message="User Created",
                    data=response_data,
                    status=status.HTTP_201_CREATED,
                ).success_message()
            return CustomResponse(
                message="validation error", data=serializer.errors
            ).error_message()
        except Exception as e:
            return CustomResponse(message=e).error_message()

    @action(methods=["get", "post"], detail=False, url_name="logout")
    def logout(self, request, *args, **kwargs):
        try:
            if request.user.is_authenticated:
                auth_logout(request)
                return CustomResponse(message="User Logged Out").success_message()
            return CustomResponse(
                message="No user logged in!", status=status.HTTP_400_BAD_REQUEST
            ).error_message()
        except Exception as e:
            return CustomResponse(message=e).error_message()


class PasswordHandlerView(viewsets.ViewSet):
    """viewset to handle forgot and change password view"""

    user_app_service = UserAppService()

    def get_serializer_class(self):
        if self.action == "forgot_password":
            return AuthSerializer
        elif self.action == "verify_otp":
            return UserCreateViewSerializer
        elif self.action == "change_password":
            return AuthSerializer

    @action(methods=["post"], detail=True, url_name="forgot-password")
    def forgot_password(self, request, pk=None, *args, **kwargs):
        serializer = self.get_serializer_class()
        # if not pk and request.user.is_authenticated:
        #     pk = request.user.id
        try:
            user = self.user_app_service.get_user_by_id(id=pk)
            if user:
                serializer = serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                response_data = self.user_app_service.forgot_password(user=user)
                return CustomResponse(data=response_data).success_message()
            return CustomResponse(message="User Doesn't Exist").error_message()
        except serializers.ValidationError:
            return CustomResponse(data=serializer.errors).error_message()
        except User.DoesNotExist:
            return CustomResponse(
                message="Otp will be sent if the user exists!"
            ).success_message()
        except Exception as e:
            return CustomResponse(message=e).error_message()

    @action(methods=["post"], detail=True, url_name="verify-otp")
    def verify_otp(self, request, pk=None, *args, **kwargs):
        pass

    @action(methods=["post"], detail=True, url_name="change-password")
    def change_password(self, request, pk=None, *args, **kwargs):
        pass


class CustomTokenRefreshView(TokenViewBase):
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                return CustomResponse(
                    message="Token Refreshed",
                    data=serializer.data,
                    status=status.HTTP_201_CREATED,
                ).success_message()
            return CustomResponse(
                message="validation error", data=serializer.errors
            ).error_message()
        except TokenError as e:
            return CustomResponse(
                message=e, status=status.HTTP_403_FORBIDDEN
            ).error_message()
