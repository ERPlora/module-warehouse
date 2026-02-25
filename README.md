# Warehouse Management Module

Warehouse zones, locations, and stock movements for managing physical storage and inventory transfers.

## Features

- Multiple warehouse support with name, code, and address
- Zone management within warehouses (storage, picking, shipping, etc.)
- Stock movement tracking with four types: inbound, outbound, transfer, and adjustment
- Source and destination zone assignment for movements
- Movement status tracking (pending, completed, etc.)
- Reference numbers and notes per movement
- Warehouse activation/deactivation
- Dashboard with warehouse activity overview

## Installation

This module is installed automatically via the ERPlora Marketplace.

## Configuration

Access settings via: **Menu > Warehouse Management > Settings**

## Usage

Access via: **Menu > Warehouse Management**

### Views

| View | URL | Description |
|------|-----|-------------|
| Dashboard | `/m/warehouse/dashboard/` | Overview of warehouse activity and statistics |
| Warehouses | `/m/warehouse/warehouses/` | Manage warehouse locations |
| Zones | `/m/warehouse/zones/` | Manage zones within warehouses |
| Movements | `/m/warehouse/movements/` | Track and create stock movements |
| Settings | `/m/warehouse/settings/` | Configure warehouse module settings |

## Models

| Model | Description |
|-------|-------------|
| `Warehouse` | Physical warehouse location with name, code, address, and active status |
| `Zone` | Named area within a warehouse (e.g., storage, receiving) with code and zone type |
| `StockMovement` | Records stock movements between zones with reference, type (inbound/outbound/transfer/adjustment), quantity, and status |

## Permissions

| Permission | Description |
|------------|-------------|
| `warehouse.view_warehouse` | View warehouses |
| `warehouse.add_warehouse` | Create new warehouses |
| `warehouse.change_warehouse` | Edit existing warehouses |
| `warehouse.delete_warehouse` | Delete warehouses |
| `warehouse.view_stockmovement` | View stock movements |
| `warehouse.add_stockmovement` | Create new stock movements |
| `warehouse.manage_settings` | Manage warehouse module settings |

## License

MIT

## Author

ERPlora Team - support@erplora.com
