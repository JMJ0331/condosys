from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('', views.AreaComunViewSet, basename='area')

urlpatterns = [
    path('agregar/', views.agregar_area_comun, name='agregar_area_comun'),
    path('actualizar/<uuid:pk>/', views.actualizar_area_comun, name='actualizar_area_comun'),
    path('eliminar/<uuid:pk>/', views.eliminar_area_comun, name='eliminar_area_comun'),
    path('', views.app_index, name='areas_comunes_index'),
    path('api/', include(router.urls)),
]
