from django.contrib import admin

from .models import Warehouse, Zone, StockMovement

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'address', 'is_active']
    readonly_fields = ['id', 'hub_id', 'created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ['warehouse', 'name', 'code', 'zone_type']
    readonly_fields = ['id', 'hub_id', 'created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['reference', 'movement_type', 'source_zone', 'dest_zone', 'quantity']
    readonly_fields = ['id', 'hub_id', 'created_at', 'updated_at']
    ordering = ['-created_at']

