from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Warehouse, StockMovement

class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ['name', 'code', 'address', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'code': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'address': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'toggle'}),
        }

class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['reference', 'movement_type', 'source_zone', 'dest_zone', 'quantity', 'notes', 'status']
        widgets = {
            'reference': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'movement_type': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'source_zone': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'dest_zone': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'quantity': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
            'notes': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 3}),
            'status': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
        }

