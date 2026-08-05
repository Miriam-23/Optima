from rest_framework import viewsets, mixins, generics, status
from django.contrib.auth.models import User
from .models import TokenVerificacion
from .models import Rol
from .serializers import UserSerializer, RolSerializer, RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import LoginSerializer
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from notifications.emails import enviar_correo_reset_password, enviar_correo_verificacion
import logging

logger = logging.getLogger(__name__)


# ----- Vista para obtener y actualizar el perfil del usuario autenticado -----
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

# ----- Vista general de usuarios ----- 
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(is_active=True) # Solo enviamos usuarios activos
    serializer_class = UserSerializer

# ----- Vista para obtener roles -----
class RolViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer

# ----- Vista para cerrar sesión -----
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'mensaje': 'Sesión cerrada correctamente.'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'error': 'Token inválido o ya expirado.'}, status=status.HTTP_400_BAD_REQUEST)

# ----- Vista para registrar un nuevo usuario -----
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]  # Este endpoint NO requiere token
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        datos = serializer.data
        correo_enviado = getattr(serializer, 'correo_enviado', True)
        datos['correo_enviado'] = correo_enviado
        datos['mensaje'] = (
            'Cuenta creada. Revisa tu correo para activarla.'
            if correo_enviado else
            'Cuenta creada, pero no pudimos enviar el correo de verificaci\u00f3n. '
            'Solicita el reenv\u00edo desde la pantalla de inicio de sesi\u00f3n.'
        )

        headers = self.get_success_headers(serializer.data)
        return Response(datos, status=status.HTTP_201_CREATED, headers=headers)


# ----- Reenviar el correo de verificaci\u00f3n -----
class ReenviarVerificacionView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        correo = request.data.get('email', '').strip().lower()

        if not correo:
            return Response(
                {'error': 'El correo electr\u00f3nico es requerido.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        respuesta_generica = Response(
            {'mensaje': 'Si esa cuenta existe y est\u00e1 pendiente, te reenviamos el enlace.'},
            status=status.HTTP_200_OK
        )

        try:
            usuario = User.objects.get(email__iexact=correo, is_active=False)
        except User.DoesNotExist:
            return respuesta_generica

        # Regeneramos el token para reiniciar las 24 horas de vigencia.
        TokenVerificacion.objects.filter(usuario=usuario).delete()
        token = TokenVerificacion.objects.create(usuario=usuario)

        try:
            enviar_correo_verificacion(usuario, token.token)
        except Exception:
            logger.exception('No se pudo reenviar la verificaci\u00f3n a %s', correo)
            return Response(
                {'error': 'No pudimos enviar el correo en este momento. Intenta m\u00e1s tarde.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        return respuesta_generica

# ----- Vista para iniciar sesión -----
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

# ----- Vista para verificar correo electrónico -----
class VerificarCorreoView(APIView):
    permission_classes = []  # No requiere token

    def get(self, request, token):
        try:
            token_obj = TokenVerificacion.objects.select_related('usuario').get(token=token)
        except TokenVerificacion.DoesNotExist:
            return Response(
                {'error': 'Enlace de verificación inválido.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if token_obj.ha_expirado():
            token_obj.delete()
            return Response(
                {'error': 'El enlace ha expirado. Regístrate nuevamente.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        usuario = token_obj.usuario
        usuario.is_active = True
        usuario.save()
        token_obj.delete()  # El token ya no sirve después de usarse

        return Response(
            {'mensaje': f'Cuenta de {usuario.username} verificada correctamente. Ya puedes iniciar sesión.'},
            status=status.HTTP_200_OK
        )

# ----- Restablecimiento de contraseña -----
class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        correo = request.data.get('email', '').strip().lower()

        if not correo:
            return Response(
                {'error': 'El correo electrónico es requerido.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            usuario = User.objects.get(email=correo, is_active=True)

            uid = urlsafe_base64_encode(force_bytes(usuario.pk))
            token = default_token_generator.make_token(usuario)

            enviar_correo_reset_password(usuario, token, uid)

        except User.DoesNotExist:
            # No revelamos si el correo existe por motivos de seguridad.
            pass

        return Response(
            {
                'mensaje': (
                    'Si ese correo está registrado, recibirás un enlace '
                    'para restablecer tu contraseña.'
                )
            },
            status=status.HTTP_200_OK
        )

# ----- Confirmación de restablecimiento de contraseña -----
class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        uid = request.data.get('uid', '').strip()
        token = request.data.get('token', '').strip()
        nueva_password = request.data.get('new_password', '').strip()

        if not uid or not token or not nueva_password:
            return Response(
                {
                    'error': 'uid, token y new_password son requeridos.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            pk = force_str(urlsafe_base64_decode(uid))
            usuario = User.objects.get(pk=pk, is_active=True)

        except (User.DoesNotExist, ValueError, TypeError):
            return Response(
                {'error': 'El enlace es inválido o ha expirado.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not default_token_generator.check_token(usuario, token):
            return Response(
                {'error': 'El enlace es inválido o ha expirado.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Utilizamos los validadores configurados en AUTH_PASSWORD_VALIDATORS
        try:
            validate_password(nueva_password, usuario)

        except ValidationError as e:
            return Response(
                {
                    'error': list(e.messages)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        usuario.set_password(nueva_password)
        usuario.save()

        return Response(
            {
                'mensaje': (
                    'Contraseña actualizada correctamente. '
                    'Ya puedes iniciar sesión.'
                )
            },
            status=status.HTTP_200_OK
        )