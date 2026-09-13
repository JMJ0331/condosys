from django.db import models

# ==================================================
# PROPIETARIOS
# ==================================================
# El módulo Propietarios no define un modelo propio:
# reutiliza `residents.Resident` a través de la relación
# `Apartment.owner` (related_name='apartments_owned') para
# listar y administrar a los propietarios de departamentos.