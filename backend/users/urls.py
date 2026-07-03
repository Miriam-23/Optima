from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RolViewSet, LogoutView, RegisterView, MeView, VerificarCorreoView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'roles', RolViewSet, basename='rol')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/me/', MeView.as_view(), name='me'),
    path('auth/verificar/<uuid:token>/', VerificarCorreoView.as_view(), name='verificar'), 
]