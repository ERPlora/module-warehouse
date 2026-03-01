"""AI tools for the Warehouse module."""
from assistant.tools import AssistantTool, register_tool


@register_tool
class ListWarehouses(AssistantTool):
    name = "list_warehouses"
    description = "List warehouses."
    module_id = "warehouse"
    required_permission = "warehouse.view_warehouse"
    parameters = {
        "type": "object",
        "properties": {"is_active": {"type": "boolean"}},
        "required": [],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from warehouse.models import Warehouse
        qs = Warehouse.objects.all()
        if 'is_active' in args:
            qs = qs.filter(is_active=args['is_active'])
        return {"warehouses": [{"id": str(w.id), "name": w.name, "code": w.code, "address": w.address, "is_active": w.is_active} for w in qs]}


@register_tool
class CreateWarehouse(AssistantTool):
    name = "create_warehouse"
    description = "Create a new warehouse."
    module_id = "warehouse"
    required_permission = "warehouse.add_warehouse"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {
            "name": {"type": "string"}, "code": {"type": "string"}, "address": {"type": "string"},
        },
        "required": ["name"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from warehouse.models import Warehouse
        w = Warehouse.objects.create(name=args['name'], code=args.get('code', ''), address=args.get('address', ''))
        return {"id": str(w.id), "name": w.name, "created": True}


@register_tool
class ListWarehouseZones(AssistantTool):
    name = "list_warehouse_zones"
    description = "List warehouse zones."
    module_id = "warehouse"
    required_permission = "warehouse.view_zone"
    parameters = {
        "type": "object",
        "properties": {"warehouse_id": {"type": "string"}},
        "required": [],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from warehouse.models import Zone
        qs = Zone.objects.select_related('warehouse').all()
        if args.get('warehouse_id'):
            qs = qs.filter(warehouse_id=args['warehouse_id'])
        return {"zones": [{"id": str(z.id), "name": z.name, "code": z.code, "zone_type": z.zone_type, "warehouse": z.warehouse.name} for z in qs]}


@register_tool
class CreateWarehouseZone(AssistantTool):
    name = "create_warehouse_zone"
    description = "Create a zone within a warehouse."
    module_id = "warehouse"
    required_permission = "warehouse.add_zone"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {
            "warehouse_id": {"type": "string"}, "name": {"type": "string"}, "code": {"type": "string"},
            "zone_type": {"type": "string", "description": "Zone type (e.g., storage, receiving, shipping)"},
        },
        "required": ["warehouse_id", "name"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from warehouse.models import Zone
        z = Zone.objects.create(
            warehouse_id=args['warehouse_id'], name=args['name'],
            code=args.get('code', ''), zone_type=args.get('zone_type', 'storage'),
        )
        return {"id": str(z.id), "name": z.name, "created": True}
