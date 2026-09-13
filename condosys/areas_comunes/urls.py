from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('', views.AreaComunViewSet, basename='area')

urlpatterns = [
    path('crear/', views.crear_area_comun, name='crear_area_comun'),
    path('', views.app_index, name='areas_comunes_index'),
    path('api/', include(router.urls)),
]