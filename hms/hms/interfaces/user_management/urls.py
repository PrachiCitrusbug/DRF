from rest_framework.routers import SimpleRouter
from .views import UserViewSet

router = SimpleRouter()
router.register(r'users', viewset=UserViewSet, basename="user")
