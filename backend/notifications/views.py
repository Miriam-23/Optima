from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Notificacion
from .serializers import NotificacionSerializer

class NotificacionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificacionSerializer

    def get_queryset(self):
        return Notificacion.objects.filter(usuario=self.request.user)

    @action(detail=False, methods=['post'], url_path='marcar-leidas')
    def marcar_leidas(self, request):
        Notificacion.objects.filter(
            usuario=request.user,
            leida=False
        ).update(leida=True)
        return Response({'mensaje': 'Notificaciones marcadas como leídas.'})