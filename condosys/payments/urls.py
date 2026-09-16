from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, app_index, agregar_pago, eliminar_pago, generar_comprobante

router = DefaultRouter()
router.register(r'registros', PaymentViewSet, basename='pago')

urlpatterns = [
    path('agregar/', agregar_pago, name='agregar_pago'),
    path('eliminar/<uuid:pk>/', eliminar_pago, name='eliminar_pago'),
    path('comprobante/', generar_comprobante, name='generar_comprobante'),
    path('', app_index, name='pagos_index'),
    path('', include(router.urls)),
]