from django.core.mail import send_mail
from django.conf import settings

def enviar_correo_notificacion(usuario, tipo, mensaje):
    if not usuario.email:
        return  # Si el usuario no tiene correo, no enviamos nada
    
    asuntos = {
        'tarea_asignada': 'Nueva tarea asignada — Optima',
        'comentario_nuevo': 'Nuevo comentario en tu tarea — Optima',
        'miembro_agregado': 'Fuiste agregado a un proyecto — Optima',
    }

    asunto = asuntos.get(tipo, 'Nueva notificación — Optima')

    cuerpo = f"""
Hola {usuario.username},

{mensaje}

Ingresa a Optima para ver más detalles.

---
Este es un mensaje automático, por favor no respondas este correo.
Optima — Gestión de Proyectos
    """.strip()

    try:
        send_mail(
            subject=asunto,
            message=cuerpo,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[usuario.email],
            fail_silently=True  # Si falla el correo, la operación principal no se interrumpe
        )
    except Exception:
        pass  # El correo es secundario, nunca debe romper el flujo principal

def enviar_correo_verificacion(usuario, token):
    # Construye el enlace de verificación usando el token
    enlace = f'http://localhost:5173/verificar/{token}'
    asunto = 'Verifica tu cuenta — Optima'
    cuerpo = f"""
Hola {usuario.username},

Gracias por registrarte en Optima. Para activar tu cuenta haz clic en el siguiente enlace:

{enlace}

Este enlace expira en 24 horas.

Si no creaste esta cuenta, ignora este correo.

---
Optima — Gestión de Proyectos
    """.strip()

    try:
        send_mail(
            subject=asunto,
            message=cuerpo,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[usuario.email],
            fail_silently=False
        )
    except Exception as e:
        print(f'Error enviando correo de verificación: {e}')