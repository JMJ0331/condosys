from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, app_index, crear_pago

router = DefaultRouter()
router.register(r'records', PaymentViewSet, basename='payment')

urlpatterns = [
    path('crear/', crear_pago, name='crear_pago'),
    path('', app_index, name='payments_index'),
    path('', include(router.urls)),
]