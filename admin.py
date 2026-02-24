from django.contrib import admin

from .models import Warehouse, Zone, StockMovement

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'is_active', 'created_at']
    search_fields = ['name', 'code', 'address']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ['warehouse', 'name', 'code', 'zone_type', 'created_at']
    search_fields = ['name', 'code', 'zone_type']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['reference', 'movement_type', 'source_zone', 'dest_zone', 'quantity', 'created_at']
    search_fields = ['reference', 'movement_type', 'notes', 'status']
    readonly_fields = ['created_at', 'updated_at']

