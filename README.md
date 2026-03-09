# Warehouse Management

## Overview

| Property | Value |
|----------|-------|
| **Module ID** | `warehouse` |
| **Version** | `1.0.0` |
| **Icon** | `home-outline` |
| **Dependencies** | None |

## Models

### `Warehouse`

Warehouse(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, name, code, address, is_active)

| Field | Type | Details |
|-------|------|---------|
| `name` | CharField | max_length=255 |
| `code` | CharField | max_length=20, optional |
| `address` | TextField | optional |
| `is_active` | BooleanField |  |

### `Zone`

Zone(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, warehouse, name, code, zone_type)

| Field | Type | Details |
|-------|------|---------|
| `warehouse` | ForeignKey | → `warehouse.Warehouse`, on_delete=CASCADE |
| `name` | CharField | max_length=255 |
| `code` | CharField | max_length=20, optional |
| `zone_type` | CharField | max_length=30 |

### `StockMovement`

StockMovement(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, reference, movement_type, source_zone, dest_zone, quantity, notes, status)

| Field | Type | Details |
|-------|------|---------|
| `reference` | CharField | max_length=50 |
| `movement_type` | CharField | max_length=20, choices: inbound, outbound, transfer, adjustment |
| `source_zone` | ForeignKey | → `warehouse.Zone`, on_delete=SET_NULL, optional |
| `dest_zone` | ForeignKey | → `warehouse.Zone`, on_delete=SET_NULL, optional |
| `quantity` | DecimalField |  |
| `notes` | TextField | optional |
| `status` | CharField | max_length=20 |

## Cross-Module Relationships

| From | Field | To | on_delete | Nullable |
|------|-------|----|-----------|----------|
| `Zone` | `warehouse` | `warehouse.Warehouse` | CASCADE | No |
| `StockMovement` | `source_zone` | `warehouse.Zone` | SET_NULL | Yes |
| `StockMovement` | `dest_zone` | `warehouse.Zone` | SET_NULL | Yes |

## URL Endpoints

Base path: `/m/warehouse/`

| Path | Name | Method |
|------|------|--------|
| `(root)` | `dashboard` | GET |
| `zones/` | `zones` | GET |
| `movements/` | `movements` | GET |
| `warehouses/` | `warehouses_list` | GET |
| `warehouses/add/` | `warehouse_add` | GET/POST |
| `warehouses/<uuid:pk>/edit/` | `warehouse_edit` | GET |
| `warehouses/<uuid:pk>/delete/` | `warehouse_delete` | GET/POST |
| `warehouses/<uuid:pk>/toggle/` | `warehouse_toggle_status` | GET |
| `warehouses/bulk/` | `warehouses_bulk_action` | GET/POST |
| `stock_movements/` | `stock_movements_list` | GET |
| `stock_movements/add/` | `stock_movement_add` | GET/POST |
| `stock_movements/<uuid:pk>/edit/` | `stock_movement_edit` | GET |
| `stock_movements/<uuid:pk>/delete/` | `stock_movement_delete` | GET/POST |
| `stock_movements/bulk/` | `stock_movements_bulk_action` | GET/POST |
| `settings/` | `settings` | GET |

## Permissions

| Permission | Description |
|------------|-------------|
| `warehouse.view_warehouse` | View Warehouse |
| `warehouse.add_warehouse` | Add Warehouse |
| `warehouse.change_warehouse` | Change Warehouse |
| `warehouse.delete_warehouse` | Delete Warehouse |
| `warehouse.view_stockmovement` | View Stockmovement |
| `warehouse.add_stockmovement` | Add Stockmovement |
| `warehouse.manage_settings` | Manage Settings |

**Role assignments:**

- **admin**: All permissions
- **manager**: `add_stockmovement`, `add_warehouse`, `change_warehouse`, `view_stockmovement`, `view_warehouse`
- **employee**: `add_warehouse`, `view_stockmovement`, `view_warehouse`

## Navigation

| View | Icon | ID | Fullpage |
|------|------|----|----------|
| Dashboard | `speedometer-outline` | `dashboard` | No |
| Warehouses | `home-outline` | `warehouses` | No |
| Zones | `grid-outline` | `zones` | No |
| Movements | `swap-horizontal-outline` | `movements` | No |
| Settings | `settings-outline` | `settings` | No |

## AI Tools

Tools available for the AI assistant:

### `list_warehouses`

List warehouses.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `is_active` | boolean | No |  |

### `create_warehouse`

Create a new warehouse.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes |  |
| `code` | string | No |  |
| `address` | string | No |  |

### `list_warehouse_zones`

List warehouse zones.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `warehouse_id` | string | No |  |

### `create_warehouse_zone`

Create a zone within a warehouse.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `warehouse_id` | string | Yes |  |
| `name` | string | Yes |  |
| `code` | string | No |  |
| `zone_type` | string | No | Zone type (e.g., storage, receiving, shipping) |

## File Structure

```
README.md
__init__.py
admin.py
ai_tools.py
apps.py
forms.py
locale/
  en/
    LC_MESSAGES/
      django.po
  es/
    LC_MESSAGES/
      django.po
migrations/
  0001_initial.py
  __init__.py
models.py
module.py
static/
  icons/
    icon.svg
  warehouse/
    css/
    js/
templates/
  warehouse/
    pages/
      dashboard.html
      index.html
      movements.html
      settings.html
      stock_movement_add.html
      stock_movement_edit.html
      stock_movements.html
      warehouse_add.html
      warehouse_edit.html
      warehouses.html
      zones.html
    partials/
      dashboard_content.html
      movements_content.html
      panel_stock_movement_add.html
      panel_stock_movement_edit.html
      panel_warehouse_add.html
      panel_warehouse_edit.html
      settings_content.html
      stock_movement_add_content.html
      stock_movement_edit_content.html
      stock_movements_content.html
      stock_movements_list.html
      warehouse_add_content.html
      warehouse_edit_content.html
      warehouses_content.html
      warehouses_list.html
      zones_content.html
tests/
  __init__.py
  conftest.py
  test_models.py
  test_views.py
urls.py
views.py
```
