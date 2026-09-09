from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, app_index

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('', app_index, name='accounts_index'),
    path('', include(router.urls)),
]
