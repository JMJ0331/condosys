from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommonAreaViewSet, ReservationViewSet

router = DefaultRouter()
router.register(r'common-areas', CommonAreaViewSet, basename='commonarea')
router.register(r'', ReservationViewSet, basename='reservation')

urlpatterns = [
    path('', include(router.urls)),
]
