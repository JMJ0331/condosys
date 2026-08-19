from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommonAreaViewSet, ReservationViewSet, app_index

router = DefaultRouter()
router.register(r'common-areas', CommonAreaViewSet, basename='commonarea')
router.register(r'', ReservationViewSet, basename='reservation')

urlpatterns = [
    path('', app_index, name='reservations_index'),
    path('', include(router.urls)),
]
