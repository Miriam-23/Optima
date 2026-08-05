import logging
from email.utils import parseaddr

import httpx
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend

logger = logging.getLogger(__name__)

TIMEOUT = 20.0


def _extraer_html(mensaje):
    """Devuelve la alternativa text/html del mensaje, si existe."""
    for contenido, mimetype in getattr(mensaje, 'alternatives', []) or []:
        if mimetype == 'text/html':
            return contenido
    return None


class _APIEmailBackendBase(BaseEmailBackend):
    """Lógica común: recorrer mensajes, contar envíos, manejar errores."""

    nombre_proveedor = 'API'

    def send_messages(self, email_messages):
        if not email_messages:
            return 0

        enviados = 0
        for mensaje in email_messages:
            try:
                self._enviar_uno(mensaje)
                enviados += 1
                logger.info(
                    'Correo enviado vía %s a %s | asunto: %s',
                    self.nombre_proveedor, mensaje.to, mensaje.subject,
                )
            except Exception:
                logger.exception(
                    'Falló el envío vía %s a %s | asunto: %s',
                    self.nombre_proveedor, mensaje.to, mensaje.subject,
                )
                if not self.fail_silently:
                    raise
        return enviados

    def _enviar_uno(self, mensaje):
        raise NotImplementedError


class BrevoAPIBackend(_APIEmailBackendBase):
    """
    Brevo (ex Sendinblue). Plan gratuito: 300 correos/día.
    Ventaja para este proyecto: basta con verificar UN remitente por correo
    (te llega un link, le das clic) y ya puedes enviarle a CUALQUIER persona.
    No necesitas dominio propio.
    """

    nombre_proveedor = 'Brevo'
    URL = 'https://api.brevo.com/v3/smtp/email'

    def _enviar_uno(self, mensaje):
        api_key = getattr(settings, 'BREVO_API_KEY', None)
        if not api_key:
            raise RuntimeError('Falta la variable de entorno BREVO_API_KEY')

        nombre, correo = parseaddr(mensaje.from_email or settings.DEFAULT_FROM_EMAIL)

        payload = {
            'sender': {'email': correo, 'name': nombre or 'Optima'},
            'to': [{'email': destino} for destino in mensaje.to],
            'subject': mensaje.subject,
            'textContent': mensaje.body,
        }

        html = _extraer_html(mensaje)
        if html:
            payload['htmlContent'] = html
        if mensaje.cc:
            payload['cc'] = [{'email': c} for c in mensaje.cc]
        if mensaje.bcc:
            payload['bcc'] = [{'email': b} for b in mensaje.bcc]
        if mensaje.reply_to:
            payload['replyTo'] = {'email': parseaddr(mensaje.reply_to[0])[1]}

        respuesta = httpx.post(
            self.URL,
            headers={
                'api-key': api_key,
                'accept': 'application/json',
                'content-type': 'application/json',
            },
            json=payload,
            timeout=TIMEOUT,
        )

        if respuesta.status_code >= 400:
            raise RuntimeError(
                f'Brevo respondió {respuesta.status_code}: {respuesta.text}'
            )


class ResendAPIBackend(_APIEmailBackendBase):
    """
    Resend. Muy cómodo, pero OJO: sin dominio verificado solo te deja enviar
    a la dirección con la que registraste la cuenta. Úsalo si ya verificaste
    un dominio propio; si no, usa Brevo.
    """

    nombre_proveedor = 'Resend'
    URL = 'https://api.resend.com/emails'

    def _enviar_uno(self, mensaje):
        api_key = getattr(settings, 'RESEND_API_KEY', None)
        if not api_key:
            raise RuntimeError('Falta la variable de entorno RESEND_API_KEY')

        payload = {
            'from': mensaje.from_email or settings.DEFAULT_FROM_EMAIL,
            'to': list(mensaje.to),
            'subject': mensaje.subject,
            'text': mensaje.body,
        }

        html = _extraer_html(mensaje)
        if html:
            payload['html'] = html
        if mensaje.cc:
            payload['cc'] = list(mensaje.cc)
        if mensaje.bcc:
            payload['bcc'] = list(mensaje.bcc)
        if mensaje.reply_to:
            payload['reply_to'] = list(mensaje.reply_to)

        respuesta = httpx.post(
            self.URL,
            headers={'Authorization': f'Bearer {api_key}'},
            json=payload,
            timeout=TIMEOUT,
        )

        if respuesta.status_code >= 400:
            raise RuntimeError(
                f'Resend respondió {respuesta.status_code}: {respuesta.text}'
            )
