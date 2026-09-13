from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, app_index, crear_pago, generar_comprobante

router = DefaultRouter()
router.register(r'registros', PaymentViewSet, basename='pago')

urlpatterns = [
    path('crear/', crear_pago, name='crear_pago'),
    path('comprobante/', generar_comprobante, name='generar_comprobante'),
    path('', app_index, name='pagos_index'),
    path('', include(router.urls)),
]