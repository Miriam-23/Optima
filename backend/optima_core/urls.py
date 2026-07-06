"""
URL configuration for optima_core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Aquí conectamos las APIS. Todas sus rutas empezarán con /api/
    path('api/', include('projects.urls')),
    path('api/', include('tasks.urls')),
    path('api/', include('users.urls')), # Habilitar Usuarios y Roles
    path('api/', include('notifications.urls')),
    path('api/', include('reports.urls')),

    # Endpoints JWT
    #path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
