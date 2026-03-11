"""
AI context for the Warehouse module.
Loaded into the assistant system prompt when this module's tools are active.
"""

CONTEXT = """
## Module Knowledge: Warehouse

### Models

**Warehouse**
- `name` (str, required), `code` (str, optional short code), `address` (text), `is_active` (bool, default True)
- Represents a physical storage facility.

**Zone**
- `warehouse` (FK → Warehouse), `name` (str), `code` (str), `zone_type` (str, default 'storage')
- Sub-areas within a warehouse (e.g. receiving, storage, dispatch). zone_type is free text.

**StockMovement**
- `reference` (str, required), `movement_type` (choices: inbound | outbound | transfer | adjustment)
- `source_zone` (FK → Zone, nullable), `dest_zone` (FK → Zone, nullable)
- `quantity` (decimal), `status` (str, default 'pending'), `notes` (text)
- For transfers: set both source_zone and dest_zone.
- For inbound: set dest_zone only. For outbound: set source_zone only.
- For adjustments: either zone can be set depending on context.

### Key Flows

1. **Create warehouse**: provide name (and optionally code, address).
2. **Add zones**: create Zone records linked to the warehouse (e.g. 'Receiving', 'Storage A', 'Dispatch').
3. **Record movement**: create StockMovement with reference, movement_type, quantity, and appropriate source/dest zones.
4. **Update movement status**: change status from 'pending' → 'done' (or similar) once movement is executed.

### Relationships

- Zone belongs to Warehouse (CASCADE delete).
- StockMovement references Zone via source_zone and dest_zone (SET_NULL on delete, both nullable).
- No direct FK to inventory/products — movements are zone-level, not product-level in this module.
"""
