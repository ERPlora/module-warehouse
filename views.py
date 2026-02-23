"""
Warehouse Management Module Views
"""
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from apps.accounts.decorators import login_required
from apps.core.htmx import htmx_view
from apps.modules_runtime.navigation import with_module_nav


@login_required
@with_module_nav('warehouse', 'dashboard')
@htmx_view('warehouse/pages/dashboard.html', 'warehouse/partials/dashboard_content.html')
def dashboard(request):
    """Dashboard view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('warehouse', 'warehouses')
@htmx_view('warehouse/pages/warehouses.html', 'warehouse/partials/warehouses_content.html')
def warehouses(request):
    """Warehouses view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('warehouse', 'zones')
@htmx_view('warehouse/pages/zones.html', 'warehouse/partials/zones_content.html')
def zones(request):
    """Zones view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('warehouse', 'movements')
@htmx_view('warehouse/pages/movements.html', 'warehouse/partials/movements_content.html')
def movements(request):
    """Movements view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('warehouse', 'settings')
@htmx_view('warehouse/pages/settings.html', 'warehouse/partials/settings_content.html')
def settings(request):
    """Settings view."""
    hub_id = request.session.get('hub_id')
    return {}

