import uuid

from django.db import models


class IntegracionIA(models.Model):
    """Configuración de la integración AI (registro único)."""

    PROVEEDORES = (
        ('gpt', 'GPT · OpenAI'),
        ('claude', 'Claude · Anthropic'),
        ('gemini', 'Gemini · Google'),
        ('llama', 'Llama · Meta'),
        ('mistral', 'Mistral AI'),
        ('deepseek', 'DeepSeek'),
        ('grok', 'Grok · xAI'),
    )

    # Modelos con visión disponibles por proveedor (id, etiqueta).
    MODELOS_POR_PROVEEDOR = {
        'gpt': [
            ('gpt-5', 'GPT-5'),
            ('gpt-4o', 'GPT-4o'),
            ('gpt-4.1', 'GPT-4.1'),
            ('gpt-4o-mini', 'GPT-4o Mini'),
            ('gpt-4.1-mini', 'GPT-4.1 Mini'),
        ],
        'claude': [
            ('claude-opus-4-20250514', 'Claude Opus 4'),
            ('claude-sonnet-4-20250514', 'Claude Sonnet 4'),
            ('claude-3-7-sonnet-20250219', 'Claude Sonnet 3.7'),
            ('claude-3-5-sonnet-20241022', 'Claude Sonnet 3.5'),
        ],
        'gemini': [
            ('gemini-2.5-pro', 'Gemini 2.5 Pro'),
            ('gemini-2.5-flash', 'Gemini 2.5 Flash'),
            ('gemini-2.0-flash', 'Gemini 2.0 Flash'),
            ('gemini-1.5-pro', 'Gemini 1.5 Pro'),
        ],
        'mistral': [
            ('pixtral-large-2411', 'Pixtral Large'),
            ('pixtral-12b-2409', 'Pixtral 12B'),
            ('mistral-medium-2505', 'Mistral Medium 3'),
            ('mistral-small-2503', 'Mistral Small 3'),
        ],
        'grok': [
            ('grok-4', 'Grok 4'),
            ('grok-3', 'Grok 3'),
            ('grok-2-vision-1212', 'Grok 2 Vision'),
        ],
        'deepseek': [],
        'llama': [],
    }

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    proveedor = models.CharField(max_length=20, choices=PROVEEDORES, default='gpt', verbose_name='Proveedor')
    modelo = models.CharField(max_length=60, default='gpt-4o', verbose_name='Modelo')
    api_key = models.CharField(max_length=255, blank=True, verbose_name='API Key')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Integración AI'
        verbose_name_plural = 'Integración AI'

    def __str__(self):
        return f'{self.get_proveedor_display()} · {self.modelo}'

    @classmethod
    def obtener_unica(cls):
        """Devuelve la única configuración guardada, o None si no existe."""
        return cls.objects.order_by('updated_at').first()

    @classmethod
    def modelos_de(cls, proveedor):
        """Lista de (id, etiqueta) del proveedor, vacía si no tiene visión."""
        return cls.MODELOS_POR_PROVEEDOR.get(proveedor, [])
