from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuditLogViewSet, ReportViewSet, app_index, crear_audit_log, crear_audit_log_detail

router = DefaultRouter()
router.register(r'audit-logs', AuditLogViewSet, basename='auditlog')

urlpatterns = [
    path('crear/audit-log/', crear_audit_log, name='crear_audit_log'),
    path('crear/detalle/', crear_audit_log_detail, name='crear_audit_log_detail'),
    path('', app_index, name='reports_index'),
    path('', include(router.urls)),
    path('summary/', ReportViewSet.as_view({'get': 'summary'}), name='report-summary'),
    path('payments/', ReportViewSet.as_view({'get': 'payments'}), name='report-payments'),
    path('occupancy/', ReportViewSet.as_view({'get': 'occupancy'}), name='report-occupancy'),
]