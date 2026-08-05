import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives

logger = logging.getLogger(__name__)

PIE = 'Optima — Gestión de Proyectos'


def _enviar(asunto, cuerpo, destinatario, html=None, fail_silently=False):
    """
    Punto único de salida de todo el correo del sistema.
    Loggea siempre (éxito y error) para que se vea en los logs de Railway.
    """
    mensaje = EmailMultiAlternatives(
        subject=asunto,
        body=cuerpo,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[destinatario],
    )
    if html:
        mensaje.attach_alternative(html, 'text/html')

    try:
        enviados = mensaje.send(fail_silently=False)
        if not enviados:
            logger.error('El proveedor no aceptó el correo para %s', destinatario)
        return bool(enviados)
    except Exception:
        logger.exception(
            'Error enviando correo a %s | asunto: %s | proveedor: %s',
            destinatario, asunto, settings.EMAIL_PROVIDER,
        )
        if not fail_silently:
            raise
        return False


def _html_basico(titulo, parrafos, boton=None):
    cuerpo = ''.join(
        f'<p style="margin:0 0 14px;line-height:1.6;color:#333;">{p}</p>'
        for p in parrafos
    )
    cta = ''
    if boton:
        texto, enlace = boton
        cta = (
            f'<p style="margin:24px 0;">'
            f'<a href="{enlace}" style="background:#1867C0;color:#fff;'
            f'padding:12px 24px;border-radius:6px;text-decoration:none;'
            f'display:inline-block;font-weight:600;">{texto}</a></p>'
            f'<p style="font-size:12px;color:#777;word-break:break-all;">'
            f'Si el botón no funciona, copia este enlace:<br>{enlace}</p>'
        )
    return (
        '<div style="font-family:Arial,Helvetica,sans-serif;max-width:560px;'
        'margin:0 auto;padding:24px;">'
        f'<h2 style="color:#1867C0;margin:0 0 16px;">{titulo}</h2>'
        f'{cuerpo}{cta}'
        '<hr style="border:none;border-top:1px solid #e0e0e0;margin:24px 0;">'
        f'<p style="font-size:12px;color:#999;">{PIE}</p>'
        '</div>'
    )


# ------ Correo de notificaciones internas ------
def enviar_correo_notificacion(usuario, tipo, mensaje):
    if not usuario.email:
        logger.info('Usuario %s no tiene correo, se omite notificación', usuario.username)
        return False

    asuntos = {
        'tarea_asignada': 'Nueva tarea asignada — Optima',
        'comentario_nuevo': 'Nuevo comentario en tu tarea — Optima',
        'miembro_agregado': 'Fuiste agregado a un proyecto — Optima',
        'tarea_vencida': 'Tienes una tarea vencida — Optima',
    }
    asunto = asuntos.get(tipo, 'Nueva notificación — Optima')

    cuerpo = (
        f'Hola {usuario.username},\n\n'
        f'{mensaje}\n\n'
        f'Ingresa a Optima para ver más detalles:\n{settings.FRONTEND_URL}/dashboard\n\n'
        '---\n'
        'Este es un mensaje automático, por favor no respondas este correo.\n'
        f'{PIE}'
    )

    html = _html_basico(
        asunto.replace(' — Optima', ''),
        [f'Hola <strong>{usuario.username}</strong>,', mensaje],
        boton=('Abrir Optima', f'{settings.FRONTEND_URL}/dashboard'),
    )

    # Las notificaciones son secundarias: si fallan, no rompen la operación.
    return _enviar(asunto, cuerpo, usuario.email, html, fail_silently=True)


# ------ Correo de verificación de cuenta ------
def enviar_correo_verificacion(usuario, token):
    enlace = f'{settings.FRONTEND_URL}/verificar/{token}'
    asunto = 'Verifica tu cuenta — Optima'

    cuerpo = (
        f'Hola {usuario.username},\n\n'
        'Gracias por registrarte en Optima. Para activar tu cuenta abre este enlace:\n\n'
        f'{enlace}\n\n'
        'Este enlace expira en 24 horas.\n\n'
        'Si no creaste esta cuenta, ignora este correo.\n\n'
        '---\n'
        f'{PIE}'
    )

    html = _html_basico(
        'Verifica tu cuenta',
        [
            f'Hola <strong>{usuario.username}</strong>,',
            'Gracias por registrarte en Optima. Para activar tu cuenta haz clic en el botón:',
            'Este enlace expira en 24 horas.',
        ],
        boton=('Activar mi cuenta', enlace),
    )

    # Este SÍ importa: si truena, que la vista se entere y responda algo útil.
    return _enviar(asunto, cuerpo, usuario.email, html, fail_silently=False)


# ----- Correo de restablecimiento de contraseña ------
def enviar_correo_reset_password(usuario, token, uid):
    enlace = f'{settings.FRONTEND_URL}/reset-password?uid={uid}&token={token}'
    asunto = 'Restablecer contraseña — Optima'

    cuerpo = (
        f'Hola {usuario.username},\n\n'
        'Recibimos una solicitud para restablecer la contraseña de tu cuenta en Optima.\n\n'
        f'Para crear una nueva contraseña abre este enlace:\n\n{enlace}\n\n'
        'Este enlace expira en 24 horas. Si no solicitaste este cambio, ignora este '
        'correo: tu contraseña no será modificada.\n\n'
        '---\n'
        f'{PIE}'
    )

    html = _html_basico(
        'Restablecer contraseña',
        [
            f'Hola <strong>{usuario.username}</strong>,',
            'Recibimos una solicitud para restablecer tu contraseña.',
            'Si no fuiste tú, ignora este correo: tu contraseña no cambiará.',
        ],
        boton=('Crear nueva contraseña', enlace),
    )

    # No revelamos al cliente si el correo existe, así que aquí sí silenciamos.
    return _enviar(asunto, cuerpo, usuario.email, html, fail_silently=True)
