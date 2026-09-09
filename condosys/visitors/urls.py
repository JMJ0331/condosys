from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VisitorViewSet, app_index

router = DefaultRouter()
router.register(r'', VisitorViewSet, basename='visitor')

urlpatterns = [
    path('', app_index, name='visitors_index'),
    path('', include(router.urls)),
]
