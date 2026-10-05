"""Lectura de cédulas con la AI configurada en el módulo.

Envía la foto del documento al proveedor elegido en Integración AI y
devuelve los 11 dígitos de la cédula dominicana, o None si no se pudo
leer. Solo usa la biblioteca estándar + Pillow (sin dependencias nuevas).
"""

import base64
import io
import json
import logging
import re
import urllib.error
import urllib.request

from PIL import Image

from .models import IntegracionIA

logger = logging.getLogger(__name__)

TIMEOUT_SEGUNDOS = 60
MAX_LADO_PX = 1280

PROMPT_CEDULA = (
    'Lee el número de cédula de identidad dominicana visible en esta '
    'imagen (formato 000-0000000-0). Responde ÚNICAMENTE con los 11 '
    'dígitos, sin guiones ni texto adicional. Si no ves ninguna cédula, '
    'responde exactamente: NADA'
)


class ErrorVision(Exception):
    """El proveedor no pudo leer la imagen (clave, red o respuesta)."""


def reducir_imagen(datos):
    """Valida que sea imagen y la reduce a JPEG liviano para el envío."""
    try:
        with Image.open(io.BytesIO(datos)) as imagen:
            imagen.verify()
        with Image.open(io.BytesIO(datos)) as imagen:
            imagen = imagen.convert('RGB')
            imagen.thumbnail((MAX_LADO_PX, MAX_LADO_PX))
            salida = io.BytesIO()
            imagen.save(salida, format='JPEG', quality=85)
            return salida.getvalue()
    except Exception:
        raise ErrorVision('El archivo no es una imagen válida.')


def extraer_digitos(texto):
    """Saca los 11 dígitos de la cédula de la respuesta del modelo."""
    if not texto or 'NADA' in texto.upper():
        return None
    digitos = re.sub(r'\D', '', texto)
    if len(digitos) < 11:
        return None
    return digitos[:11]


def con_guiones(digitos):
    """11 dígitos -> formato 000-0000000-0."""
    return f'{digitos[:3]}-{digitos[3:10]}-{digitos[10:11]}'


def _mensaje_simple(codigo, detalle):
    """Traduce un fallo del proveedor a un mensaje sencillo (sin tecnicismos)."""
    texto = f'{codigo or ""} {detalle or ""}'.lower()
    if (codigo in (401, 403) or 'unauthorized' in texto or 'unauthenticated' in texto
            or 'api key' in texto or 'apikey' in texto or 'invalid key' in texto):
        return 'La API Key no es válida. Revísala en Integración AI.'
    if (codigo == 404 or 'not found' in texto or 'does not exist' in texto
            or 'model_not_found' in texto):
        return 'El modelo no está disponible. Elige otro en Integración AI.'
    if (codigo == 429 or 'quota' in texto or 'rate_limit' in texto
            or 'rate limit' in texto or 'too many requests' in texto):
        return 'Se alcanzó el límite del proveedor. Intenta más tarde.'
    if (codigo in (500, 502, 503, 529) or 'overload' in texto
            or 'capacity' in texto or 'try again' in texto):
        return 'El proveedor está ocupado. Intenta de nuevo.'
    return 'El proveedor no pudo leer la imagen. Intenta de nuevo.'


def _post_json(url, cuerpo, cabeceras):
    """POST JSON con urllib; traduce errores HTTP a ErrorVision.

    El usuario solo ve el mensaje sencillo; el detalle técnico queda en
    el log del servidor para diagnosticar.
    """
    peticion = urllib.request.Request(
        url,
        data=json.dumps(cuerpo).encode('utf-8'),
        headers={'Content-Type': 'application/json', **cabeceras},
        method='POST',
    )
    try:
        with urllib.request.urlopen(peticion, timeout=TIMEOUT_SEGUNDOS) as respuesta:
            return json.loads(respuesta.read().decode('utf-8'))
    except urllib.error.HTTPError as error:
        try:
            detalle = json.loads(error.read().decode('utf-8'))
            err = detalle.get('error', {})
            mensaje_tecnico = (err.get('message') if isinstance(err, dict) else err) or error.reason
        except Exception:
            mensaje_tecnico = error.reason
        logger.warning('Integración AI: HTTP %s: %s', error.code, mensaje_tecnico)
        raise ErrorVision(_mensaje_simple(error.code, str(mensaje_tecnico)))
    except urllib.error.URLError as error:
        logger.warning('Integración AI: conexión: %s', error.reason)
        raise ErrorVision('No se pudo conectar con el proveedor. Revisa tu internet e intenta de nuevo.')


def _texto_openai(respuesta):
    """Lee el texto de una respuesta estilo chat/completions."""
    try:
        contenido = respuesta['choices'][0]['message']['content']
    except (KeyError, IndexError, TypeError):
        raise ErrorVision('El proveedor no devolvió una lectura válida. Intenta de nuevo.')
    if isinstance(contenido, list):
        return ''.join(
            parte.get('text', '') for parte in contenido if isinstance(parte, dict)
        )
    return contenido or ''


def _leer_openai(base_url, api_key, modelo_id, imagen_b64):
    respuesta = _post_json(
        f'{base_url}/chat/completions',
        {
            'model': modelo_id,
            'messages': [{
                'role': 'user',
                'content': [
                    {'type': 'text', 'text': PROMPT_CEDULA},
                    {'type': 'image_url', 'image_url': {
                        'url': f'data:image/jpeg;base64,{imagen_b64}',
                    }},
                ],
            }],
            'max_tokens': 50,
        },
        {'Authorization': f'Bearer {api_key}'},
    )
    return _texto_openai(respuesta)


def _leer_claude(api_key, imagen_b64, modelo):
    respuesta = _post_json(
        'https://api.anthropic.com/v1/messages',
        {
            'model': modelo,
            'max_tokens': 50,
            'messages': [{
                'role': 'user',
                'content': [
                    {
                        'type': 'image',
                        'source': {
                            'type': 'base64',
                            'media_type': 'image/jpeg',
                            'data': imagen_b64,
                        },
                    },
                    {'type': 'text', 'text': PROMPT_CEDULA},
                ],
            }],
        },
        {'x-api-key': api_key, 'anthropic-version': '2023-06-01'},
    )
    try:
        bloques = respuesta.get('content', [])
    except AttributeError:
        raise ErrorVision('El proveedor no devolvió una lectura válida. Intenta de nuevo.')
    return ''.join(
        bloque.get('text', '') for bloque in bloques if isinstance(bloque, dict)
    )


def _leer_gemini(api_key, imagen_b64, modelo):
    respuesta = _post_json(
        'https://generativelanguage.googleapis.com/v1beta/'
        f'models/{modelo}:generateContent'
        f'?key={api_key}',
        {
            'contents': [{
                'parts': [
                    {'text': PROMPT_CEDULA},
                    {'inline_data': {
                        'mime_type': 'image/jpeg',
                        'data': imagen_b64,
                    }},
                ],
            }],
        },
        {},
    )
    try:
        partes = respuesta['candidates'][0]['content']['parts']
    except (KeyError, IndexError, TypeError):
        raise ErrorVision('El proveedor no devolvió una lectura válida. Intenta de nuevo.')
    return ''.join(
        parte.get('text', '') for parte in partes if isinstance(parte, dict)
    )


# Proveedores sin API de visión directa: se avisa antes de intentar.
SIN_VISION = {
    'deepseek': 'DeepSeek no soporta lectura de imágenes; elige otro modelo en Integración AI.',
    'llama': 'Llama no expone API directa de visión; elige otro modelo en Integración AI.',
}

def extraer_cedula(proveedor, modelo, api_key, datos_imagen):
    """Lee la cédula con el proveedor y modelo configurados.

    Devuelve los 11 dígitos o None si no se pudo leer.
    """
    if proveedor in SIN_VISION:
        raise ErrorVision(SIN_VISION[proveedor])

    datos = reducir_imagen(datos_imagen)

    if not api_key:
        raise ErrorVision('Configura la API Key en Integración AI.')
    if not modelo:
        modelos = IntegracionIA.modelos_de(proveedor)
        modelo = modelos[0][0] if modelos else ''

    imagen_b64 = base64.b64encode(datos).decode('ascii')

    if proveedor == 'claude':
        texto = _leer_claude(api_key, imagen_b64, modelo)
    elif proveedor == 'gemini':
        texto = _leer_gemini(api_key, imagen_b64, modelo)
    elif proveedor == 'grok':
        texto = _leer_openai('https://api.x.ai/v1', api_key, modelo, imagen_b64)
    elif proveedor == 'mistral':
        texto = _leer_openai('https://api.mistral.ai/v1', api_key, modelo, imagen_b64)
    else:  # 'gpt' y cualquier otro compatible con OpenAI
        texto = _leer_openai('https://api.openai.com/v1', api_key, modelo or 'gpt-4o', imagen_b64)
    return extraer_digitos(texto)
