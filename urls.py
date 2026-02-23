from django.urls import path
from . import views

app_name = 'warehouse'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('warehouses/', views.warehouses, name='warehouses'),
    path('zones/', views.zones, name='zones'),
    path('movements/', views.movements, name='movements'),
    path('settings/', views.settings, name='settings'),
]
