"""
URL configuration for CONDOSYS project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# API v1 URL configuration
api_v1_patterns = [
    path('auth/', include('accounts.urls')),
    path('structure/', include('structure.urls')),
    path('residents/', include('residents.urls')),
    path('payments/', include('payments.urls')),
    path('incidents/', include('incidents.urls')),
    path('visitors/', include('visitors.urls')),
    path('reservations/', include('reservations.urls')),
    path('maintenance/', include('maintenance.urls')),
    path('communications/', include('communications.urls')),
    path('notifications/', include('notifications.urls')),
    path('chat/', include('chat.urls')),
    path('reports/', include('reports.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_v1_patterns)),
    path('api-auth/', include('rest_framework.urls')),
]

