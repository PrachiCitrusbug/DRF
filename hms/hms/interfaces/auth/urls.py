from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import AuthenticateUserView, PasswordHandlerView, CustomTokenRefreshView

router = DefaultRouter()
router.register(r'', viewset=AuthenticateUserView, basename="auth")
router.register(r'auth', viewset=PasswordHandlerView, basename="pwd")

urlpatterns = [
    path("refresh/", CustomTokenRefreshView.as_view(), name="refresh_token"),
]