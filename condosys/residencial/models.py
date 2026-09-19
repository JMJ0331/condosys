import uuid

from django.db import models

# Provincias de República Dominicana (lista fija pedida para el select).
PROVINCIAS_RD = [
    ('Distrito Nacional', 'Distrito Nacional'),
    ('Azua', 'Azua'),
    ('Baoruco', 'Baoruco'),
    ('Barahona', 'Barahona'),
    ('Dajabón', 'Dajabón'),
    ('Duarte', 'Duarte'),
    ('Elías Piña', 'Elías Piña'),
    ('El Seibo', 'El Seibo'),
    ('Espaillat', 'Espaillat'),
    ('Independencia', 'Independencia'),
    ('La Altagracia', 'La Altagracia'),
    ('La Romana', 'La Romana'),
    ('La Vega', 'La Vega'),
    ('María Trinidad Sánchez', 'María Trinidad Sánchez'),
    ('Monte Cristi', 'Monte Cristi'),
    ('Pedernales', 'Pedernales'),
    ('Peravia', 'Peravia'),
    ('Puerto Plata', 'Puerto Plata'),
    ('Hermanas Mirabal', 'Hermanas Mirabal'),
    ('Samaná', 'Samaná'),
    ('San Cristóbal', 'San Cristóbal'),
    ('San Juan', 'San Juan'),
    ('San Pedro de Macorís', 'San Pedro de Macorís'),
    ('Sánchez Ramírez', 'Sánchez Ramírez'),
    ('Santiago', 'Santiago'),
    ('Santiago Rodríguez', 'Santiago Rodríguez'),
    ('Valverde', 'Valverde'),
    ('Monseñor Nouel', 'Monseñor Nouel'),
    ('Monte Plata', 'Monte Plata'),
    ('Hato Mayor', 'Hato Mayor'),
    ('San José de Ocoa', 'San José de Ocoa'),
    ('Santo Domingo', 'Santo Domingo'),
]

# Municipios/ciudades principales por provincia para el select dependiente.
# El JS filtra por provincia; el servidor acepta cualquier valor no vacío.
MUNICIPIOS_POR_PROVINCIA = {
    'Distrito Nacional': ['Santo Domingo de Guzmán'],
    'Azua': ['Azua de Compostela', 'Las Charcas', 'Padre Las Casas', 'Peralta'],
    'Baoruco': ['Neiba', 'Galván', 'Los Ríos', 'Tamayo', 'Villa Jaragua'],
    'Barahona': ['Barahona', 'Cabral', 'Enriquillo', 'Paraíso', 'Vicente Noble'],
    'Dajabón': ['Dajabón', 'El Pino', 'Loma de Cabrera', 'Partido', 'Restauración'],
    'Duarte': ['San Francisco de Macorís', 'Castillo', 'Las Guáranas', 'Pimentel', 'Villa Riva'],
    'Elías Piña': ['Comendador', 'Bánica', 'El Llano', 'Hondo Valle', 'Pedro Santana'],
    'El Seibo': ['El Seibo', 'Miches'],
    'Espaillat': ['Moca', 'Cayetano Germosén', 'Gaspar Hernández', 'Jamao al Norte'],
    'Independencia': ['Jimaní', 'Duvergé', 'La Descubierta', 'Mella', 'Postrer Río'],
    'La Altagracia': ['Higüey', 'San Rafael del Yuma', 'Verón-Punta Cana'],
    'La Romana': ['La Romana', 'Guaymate', 'Villa Hermosa'],
    'La Vega': ['La Vega', 'Constanza', 'Jarabacoa', 'Jima Abajo'],
    'María Trinidad Sánchez': ['Nagua', 'Cabrera', 'El Factor', 'Río San Juan'],
    'Monte Cristi': ['Monte Cristi', 'Castañuelas', 'Guayubín', 'Las Matas de Santa Cruz', 'Pepillo Salcedo', 'Villa Vásquez'],
    'Pedernales': ['Pedernales', 'Oviedo'],
    'Peravia': ['Baní', 'Matanzas', 'Nizao'],
    'Puerto Plata': ['Puerto Plata', 'Altamira', 'Guananico', 'Imbert', 'Los Hidalgos', 'Luperón', 'Sosúa', 'Villa Isabela', 'Villa Montellano'],
    'Hermanas Mirabal': ['Salcedo', 'Tenares', 'Villa Tapia'],
    'Samaná': ['Samaná', 'Las Terrenas', 'Sánchez'],
    'San Cristóbal': ['San Cristóbal', 'Bajos de Haina', 'Cambita Garabitos', 'Nigua', 'Sabana Grande de Palenque', 'San Gregorio de Nigua', 'Villa Altagracia', 'Yaguate'],
    'San Juan': ['San Juan de la Maguana', 'Bohechío', 'El Cercado', 'Juan de Herrera', 'Las Matas de Farfán', 'Vallejuelo'],
    'San Pedro de Macorís': ['San Pedro de Macorís', 'Consuelo', 'Guayacanes', 'Quisqueya', 'Ramón Santana'],
    'Sánchez Ramírez': ['Cotuí', 'Cevicos', 'Fantino', 'La Mata'],
    'Santiago': ['Santiago de los Caballeros', 'Bisonó', 'Jánico', 'Licey al Medio', 'Puñal', 'Sabana Iglesia', 'San José de las Matas', 'Tamboril', 'Villa Bisonó', 'Villa González'],
    'Santiago Rodríguez': ['Sabaneta', 'Monción', 'Villa Los Almácigos'],
    'Valverde': ['Mao', 'Esperanza', 'Laguna Salada'],
    'Monseñor Nouel': ['Bonao', 'Maimón', 'Piedra Blanca'],
    'Monte Plata': ['Monte Plata', 'Bayaguana', 'Sabana Grande de Boyá', 'Yamasá'],
    'Hato Mayor': ['Hato Mayor del Rey', 'El Valle', 'Sabana de la Mar'],
    'San José de Ocoa': ['San José de Ocoa', 'Rancho Arriba', 'Sabana Larga'],
    'Santo Domingo': ['Santo Domingo Este', 'Santo Domingo Oeste', 'Santo Domingo Norte', 'Boca Chica', 'Los Alcarrizos', 'Pedro Brand', 'San Antonio de Guerra'],
}

DISTRIBUCION_CHOICES = (
    ('torres', 'Torres'),
    ('edificios', 'Edificios'),
)


class Residencial(models.Model):
    """Información genérica del residencial dueño del sistema (registro único)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Información general
    nombre = models.CharField(max_length=150, verbose_name='Nombre del residencial')
    rnc = models.CharField(max_length=11, blank=True, verbose_name='RNC')

    # Dirección
    nombre_via = models.CharField(max_length=150, blank=True, verbose_name='Nombre de la vía')
    numero_edificacion = models.CharField(max_length=30, blank=True, verbose_name='Número de la edificación')
    sector = models.CharField(max_length=120, blank=True, verbose_name='Sector')
    codigo_postal = models.CharField(max_length=10, blank=True, verbose_name='Código Postal')
    municipio = models.CharField(max_length=120, blank=True, verbose_name='Municipio/Ciudad')
    provincia = models.CharField(max_length=60, blank=True, choices=PROVINCIAS_RD, verbose_name='Provincia')
    mapa_iframe = models.TextField(blank=True, verbose_name='Iframe de Google Map')

    # Estructura
    distribucion = models.CharField(max_length=20, blank=True, choices=DISTRIBUCION_CHOICES, verbose_name='Distribución')
    cantidad_edificios = models.PositiveIntegerField(null=True, blank=True, verbose_name='Cantidad de edificios/torres')
    cantidad_pisos = models.PositiveIntegerField(null=True, blank=True, verbose_name='Cantidad de pisos por edificio/torre')

    # Contacto y administración
    telefono = models.CharField(max_length=12, blank=True, verbose_name='Teléfono de administración')
    correo = models.EmailField(max_length=254, blank=True, verbose_name='Correo de administración')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Residencial'
        verbose_name_plural = 'Residencial'

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        # La distribución solo se guarda una vez: en actualizaciones se
        # conserva el valor original aunque se intente cambiar (form, API o admin).
        if self.pk:
            original = (
                type(self).objects.filter(pk=self.pk)
                .values_list('distribucion', flat=True)
                .first()
            )
            if original:
                self.distribucion = original
        super().save(*args, **kwargs)

    @classmethod
    def obtener_unico(cls):
        """Devuelve el único registro del residencial, o None si no existe."""
        return cls.objects.order_by('created_at').first()
