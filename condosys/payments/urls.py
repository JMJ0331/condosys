from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChargeTypeViewSet, PaymentViewSet

router = DefaultRouter()
router.register(r'charge-types', ChargeTypeViewSet, basename='chargetype')
router.register(r'', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
]
