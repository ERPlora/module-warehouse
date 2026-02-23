    from django.utils.translation import gettext_lazy as _

    MODULE_ID = 'warehouse'
    MODULE_NAME = _('Warehouse Management')
    MODULE_VERSION = '1.0.0'
    MODULE_ICON = 'home-outline'
    MODULE_DESCRIPTION = _('Warehouse zones, locations and stock movements')
    MODULE_AUTHOR = 'ERPlora'
    MODULE_CATEGORY = 'commerce'

    MENU = {
        'label': _('Warehouse Management'),
        'icon': 'home-outline',
        'order': 16,
    }

    NAVIGATION = [
        {'label': _('Dashboard'), 'icon': 'speedometer-outline', 'id': 'dashboard'},
{'label': _('Warehouses'), 'icon': 'home-outline', 'id': 'warehouses'},
{'label': _('Zones'), 'icon': 'grid-outline', 'id': 'zones'},
{'label': _('Movements'), 'icon': 'swap-horizontal-outline', 'id': 'movements'},
{'label': _('Settings'), 'icon': 'settings-outline', 'id': 'settings'},
    ]

    DEPENDENCIES = []

    PERMISSIONS = [
        'warehouse.view_warehouse',
'warehouse.add_warehouse',
'warehouse.change_warehouse',
'warehouse.delete_warehouse',
'warehouse.view_stockmovement',
'warehouse.add_stockmovement',
'warehouse.manage_settings',
    ]
