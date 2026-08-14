from django.urls import path, include
from .views import *


urlpatterns = [

    path('', login_view, name='index'),
]
