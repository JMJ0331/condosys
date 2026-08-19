from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChargeTypeViewSet, PaymentViewSet, app_index

router = DefaultRouter()
router.register(r'charge-types', ChargeTypeViewSet, basename='chargetype')
router.register(r'', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', app_index, name='payments_index'),
    path('', include(router.urls)),
]
