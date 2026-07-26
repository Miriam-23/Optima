from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import ChatInputSerializer
from .services import ChatbotService

class ChatbotView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChatInputSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        mensaje = serializer.validated_data['message']
        servicio = ChatbotService()
        respuesta = servicio.obtener_respuesta(mensaje, usuario=request.user) # pasamos al usuario autenticado para personalizar la respuesta

        return Response({'response': respuesta}, status=status.HTTP_200_OK)