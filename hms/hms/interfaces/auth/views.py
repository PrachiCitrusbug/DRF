from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.urls import reverse


from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import IsAuthenticated


from .serializers import AuthSerializer, PasswordForgetSerializer, OTPSerializer, TokenSerializer, NewPasswordSerializer
from ..user_management.serializers import UserCreateViewSerializer
from hms.application.user_management.services import UserAppService
from lib.django.custom_response import CustomResponse
from lib.django.custom_permissions import IsNotAuthenticated


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
                if user:
                    response_data = self.user_app_service.get_user_token(user)
                    return CustomResponse(
                        message="Logged In", data=response_data
                    ).success_message()
                return CustomResponse("Invalid email or password!").success_message()
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
    permission_classes = [IsNotAuthenticated]

    def get_serializer_class(self):
        if self.action == "forgot_password":
            return PasswordForgetSerializer
        elif self.action == "verify_otp":
            return OTPSerializer
        elif self.action == 'reset_password':
            return TokenSerializer

    @action(methods=["post"], detail=False, url_name="forgot-password")
    def forgot_password(self, request, *args, **kwargs):
        """
        handle forgot password view
        requires email in post data
        """
        serializer = self.get_serializer_class()
        try:
            serializer = serializer(data=request.data)
            if serializer.is_valid():
                user = self.user_app_service.get_user_by_email(serializer.data.get("email"))
                if user:
                    response_data = self.user_app_service.forgot_password(user=user)
                    return CustomResponse(data=response_data).success_message()
                return CustomResponse(
                        message="Otp will be sent if the user exists!"
                    ).success_message()
            return CustomResponse(data=serializer.errors).error_message() 
        except Exception as e:
            return CustomResponse(message=e).error_message()

    @action(methods=["post"], detail=True, url_name="verify-otp")
    def verify_otp(self, request, pk, *args, **kwargs):
        """verify otp, requires otp in post data"""
        serializer = self.get_serializer_class()
        try:
            user = self.user_app_service.get_active_user_by_id(id=pk)
            if user:
                serializer = serializer(data=request.data)
                if serializer.is_valid():
                    # run verify otp here
                    otp = self.user_app_service.verify_otp(serializer.data['otp'], user.id)
                    if otp:
                        response_data = {"reset": f"{reverse('pwd-reset-password', kwargs={'pk':user.id})}?token={otp.otp_token}"}
                        return CustomResponse(data=response_data).success_message()
                    return CustomResponse(message="OTP doesn't match").error_message()
                return CustomResponse(data=serializer.errors).error_message()
            return CustomResponse(message="No User Found!").error_message()
        except Exception as e:
            return CustomResponse(message=e).error_message()

    @action(methods=["post"], detail=True, url_name="reset-password")
    def reset_password(self, request, pk, *args, **kwargs):
        """
        reset password
        id in url
        token in url get params
        new_password in post data
        """
        serializer = self.get_serializer_class()
        try:
            user = self.user_app_service.get_active_user_by_id(id=pk)
            if user:
                data = {'user_id': user.id, 'otp_token': request.GET.get('token'), 'new_password':request.data.get('new_password')}
                serializer = serializer(data=data)
                if serializer.is_valid():
                    return CustomResponse("New password successfully set!").success_message()
                return CustomResponse(data=serializer.errors).error_message()
            return CustomResponse(message="No User Found!").error_message()
        except Exception as e:
            return CustomResponse(message=e).error_message()

class ChangePasswordView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    user_app_service = UserAppService()

    @action(methods=["post"], detail=False, url_name="change-password")
    def change_password(self, request, *args, **kwargs):
        """change password view, provide old_password and new_password in the dict"""
        try:
            user = self.user_app_service.get_active_user_by_id(id=request.user.id)
            old_password = request.data.get("old_password")
            if user and old_password and authenticate(email=user.email, password=old_password):
                serializer = NewPasswordSerializer(data=request.data)
                if serializer.is_valid():
                    self.user_app_service.set_new_password(user_id=user.id, new_password=serializer.data.get("new_password"))
                    return CustomResponse("New Password successfully set!").success_message()   
                return CustomResponse(data=serializer.errors).error_message()
            return CustomResponse(message="No User Found! Please provide correct old_password.").error_message()
        except Exception as e:
            return CustomResponse(message=e).error_message()

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
