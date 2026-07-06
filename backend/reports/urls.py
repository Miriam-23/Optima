from django.urls import path
from .views import ReporteView

urlpatterns = [
    path('reports/', ReporteView.as_view(), name='reportes'),
]