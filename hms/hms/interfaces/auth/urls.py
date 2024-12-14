from django.urls import path

from rest_framework.routers import SimpleRouter

from .views import AuthenticateUserView, PasswordHandlerView, CustomTokenRefreshView, ChangePasswordView

router = SimpleRouter()
router.register(r'auth', viewset=AuthenticateUserView, basename="auth")
router.register(r'auth', viewset=PasswordHandlerView, basename="pwd")
router.register(r'auth', viewset=ChangePasswordView, basename="pwd-change")

urlpatterns = [
    path("refresh/", CustomTokenRefreshView.as_view(), name="refresh_token"),
]

urlpatterns += router.urls