from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ChargeTypeViewSet, PaymentViewSet, app_index,
    crear_pago, crear_tipo_cargo,
)

router = DefaultRouter()
router.register(r'charge-types', ChargeTypeViewSet, basename='chargetype')
router.register(r'records', PaymentViewSet, basename='payment')

urlpatterns = [
    path('crear/tipo-cargo/', crear_tipo_cargo, name='crear_tipo_cargo'),
    path('crear/', crear_pago, name='crear_pago'),
    path('', app_index, name='payments_index'),
    path('', include(router.urls)),
]