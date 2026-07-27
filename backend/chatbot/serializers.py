from rest_framework import serializers

class ChatInputSerializer(serializers.Serializer):
    message = serializers.CharField(
        max_length=2000,
        allow_blank=False,
        error_messages={
            'blank': 'El mensaje no puede estar vacío.',
            'max_length': 'El mensaje no puede superar los 2000 caracteres.',
        }
    )