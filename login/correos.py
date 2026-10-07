"""
Envío del correo transaccional de recuperación de contraseña vía Resend.

La configuración vive en settings.py (bloque "Email Configuration"):
    RESEND_API_KEY -> clave privada de la API de Resend (re_...)
    RESEND_FROM    -> remitente verificado (por defecto
                      "CONDYSOS <onboarding@resend.dev>")
"""

import logging

import resend
from django.conf import settings

logger = logging.getLogger(__name__)

ASUNTO = 'Solicitud de restablecimiento de contraseña'


def _cuerpo_correo(nombre, enlace):
    return f"""
    <div style="font-family: Arial, Helvetica, sans-serif; max-width: 480px; margin: 0 auto; color: #41413D;">
      <h2 style="color: #163D1F; font-size: 20px; margin-bottom: 16px;">Hola {nombre},</h2>
      <p style="font-size: 15px; line-height: 1.6; margin-bottom: 24px;">
        Recibimos una solicitud para restablecer la contraseña de tu cuenta en CONDYSOS.
        Para elegir una nueva contraseña, usa el botón de abajo:
      </p>
      <p style="margin-bottom: 24px;">
        <a href="{enlace}"
           style="background-color: #163D1F; color: #fefefe; padding: 12px 24px;
                  border-radius: 8px; text-decoration: none; font-weight: bold; display: inline-block;">
          Restablecer contraseña
        </a>
      </p>
      <p style="font-size: 13px; line-height: 1.6; color: #929290; margin-bottom: 8px;">
        Si el botón no funciona, copia y pega este enlace en tu navegador:
      </p>
      <p style="font-size: 13px; word-break: break-all; margin-bottom: 24px;">
        <a href="{enlace}" style="color: #3da755;">{enlace}</a>
      </p>
      <p style="font-size: 13px; line-height: 1.6; color: #60605d; border-top: 1px solid #E7E7E7; padding-top: 16px;">
        <strong>Si no solicitaste este cambio, puedes ignorar este correo de forma segura.
        Tu contraseña seguirá siendo la misma.</strong>
      </p>
      <p style="font-size: 13px; color: #929290; margin-top: 16px;">Equipo CONDYSOS</p>
    </div>
    """


def enviar_correo_recuperacion(user, enlace):
    """
    Envía el correo con el enlace de restablecimiento usando Resend.
    Lanza excepción si falta la API key o el envío falla; el llamador
    decide cómo reportarlo sin exponer si el usuario existe.
    """
    api_key = settings.RESEND_API_KEY
    if not api_key:
        if settings.DEBUG:
            logger.warning(
                'RESEND_API_KEY no configurada; enlace de recuperación (solo DEBUG): %s',
                enlace,
            )
        raise RuntimeError('RESEND_API_KEY no está configurada en .env')

    resend.api_key = api_key

    nombre = user.full_name or user.email
    remitente = settings.RESEND_FROM

    try:
        resend.Emails.send({
            'from': remitente,
            'to': [user.email],
            'subject': ASUNTO,
            'html': _cuerpo_correo(nombre, enlace),
        })
    except Exception:
        logger.exception('Falló el envío del correo de recuperación a %s', user.email)
        raise

    logger.info('Correo de recuperación enviado a %s', user.email)
