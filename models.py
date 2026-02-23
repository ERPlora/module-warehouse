from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import HubBaseModel

MOVEMENT_TYPE = [
    ('inbound', _('Inbound')),
    ('outbound', _('Outbound')),
    ('transfer', _('Transfer')),
    ('adjustment', _('Adjustment')),
]

class Warehouse(HubBaseModel):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    code = models.CharField(max_length=20, blank=True, verbose_name=_('Code'))
    address = models.TextField(blank=True, verbose_name=_('Address'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))

    class Meta(HubBaseModel.Meta):
        db_table = 'warehouse_warehouse'

    def __str__(self):
        return self.name


class Zone(HubBaseModel):
    warehouse = models.ForeignKey('Warehouse', on_delete=models.CASCADE, related_name='zones')
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    code = models.CharField(max_length=20, blank=True, verbose_name=_('Code'))
    zone_type = models.CharField(max_length=30, default='storage', verbose_name=_('Zone Type'))

    class Meta(HubBaseModel.Meta):
        db_table = 'warehouse_zone'

    def __str__(self):
        return self.name


class StockMovement(HubBaseModel):
    reference = models.CharField(max_length=50, verbose_name=_('Reference'))
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPE, verbose_name=_('Movement Type'))
    source_zone = models.ForeignKey('Zone', on_delete=models.SET_NULL, null=True, blank=True, related_name='outgoing')
    dest_zone = models.ForeignKey('Zone', on_delete=models.SET_NULL, null=True, blank=True, related_name='incoming')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Quantity'))
    notes = models.TextField(blank=True, verbose_name=_('Notes'))
    status = models.CharField(max_length=20, default='pending', verbose_name=_('Status'))

    class Meta(HubBaseModel.Meta):
        db_table = 'warehouse_stockmovement'

    def __str__(self):
        return self.reference

