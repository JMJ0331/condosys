from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuditLogViewSet, ReportViewSet, app_index, crear_audit_log, crear_audit_log_detail

router = DefaultRouter()
router.register(r'bitacoras', AuditLogViewSet, basename='bitacora')

urlpatterns = [
    path('crear/bitacora/', crear_audit_log, name='crear_bitacora'),
    path('crear/detalle/', crear_audit_log_detail, name='crear_detalle_bitacora'),
    path('', app_index, name='reportes_index'),
    path('', include(router.urls)),
    path('resumen/', ReportViewSet.as_view({'get': 'summary'}), name='reporte_resumen'),
    path('pagos/', ReportViewSet.as_view({'get': 'payments'}), name='reporte_pagos'),
    path('ocupacion/', ReportViewSet.as_view({'get': 'occupancy'}), name='reporte_ocupacion'),
]