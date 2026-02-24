from django.urls import path
from . import views

app_name = 'warehouse'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Warehouse
    path('warehouses/', views.warehouses_list, name='warehouses_list'),
    path('warehouses/add/', views.warehouse_add, name='warehouse_add'),
    path('warehouses/<uuid:pk>/edit/', views.warehouse_edit, name='warehouse_edit'),
    path('warehouses/<uuid:pk>/delete/', views.warehouse_delete, name='warehouse_delete'),
    path('warehouses/<uuid:pk>/toggle/', views.warehouse_toggle_status, name='warehouse_toggle_status'),
    path('warehouses/bulk/', views.warehouses_bulk_action, name='warehouses_bulk_action'),

    # StockMovement
    path('stock_movements/', views.stock_movements_list, name='stock_movements_list'),
    path('stock_movements/add/', views.stock_movement_add, name='stock_movement_add'),
    path('stock_movements/<uuid:pk>/edit/', views.stock_movement_edit, name='stock_movement_edit'),
    path('stock_movements/<uuid:pk>/delete/', views.stock_movement_delete, name='stock_movement_delete'),
    path('stock_movements/bulk/', views.stock_movements_bulk_action, name='stock_movements_bulk_action'),

    # Settings
    path('settings/', views.settings_view, name='settings'),
]
