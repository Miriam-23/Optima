from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RolViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'roles', RolViewSet, basename='rol')

urlpatterns = [
    path('', include(router.urls)),
]