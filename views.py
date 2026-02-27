"""
Warehouse Management Module Views
"""
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, render as django_render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from apps.accounts.decorators import login_required, permission_required
from apps.core.htmx import htmx_view
from apps.core.services import export_to_csv, export_to_excel
from apps.modules_runtime.navigation import with_module_nav

from .models import Warehouse, Zone, StockMovement

PER_PAGE_CHOICES = [10, 25, 50, 100]


# ======================================================================
# Dashboard
# ======================================================================

@login_required
@with_module_nav('warehouse', 'dashboard')
@htmx_view('warehouse/pages/index.html', 'warehouse/partials/dashboard_content.html')
def dashboard(request):
    hub_id = request.session.get('hub_id')
    return {
        'total_warehouses': Warehouse.objects.filter(hub_id=hub_id, is_deleted=False).count(),
        'total_stock_movements': StockMovement.objects.filter(hub_id=hub_id, is_deleted=False).count(),
    }


# ======================================================================
# Warehouse
# ======================================================================

WAREHOUSE_SORT_FIELDS = {
    'code': 'code',
    'name': 'name',
    'is_active': 'is_active',
    'address': 'address',
    'created_at': 'created_at',
}

def _build_warehouses_context(hub_id, per_page=10):
    qs = Warehouse.objects.filter(hub_id=hub_id, is_deleted=False).order_by('code')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'warehouses': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'code',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_warehouses_list(request, hub_id, per_page=10):
    ctx = _build_warehouses_context(hub_id, per_page)
    return django_render(request, 'warehouse/partials/warehouses_list.html', ctx)

@login_required
@with_module_nav('warehouse', 'warehouses')
@htmx_view('warehouse/pages/warehouses.html', 'warehouse/partials/warehouses_content.html')
def warehouses_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'code')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = Warehouse.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(name__icontains=search_query) | Q(code__icontains=search_query) | Q(address__icontains=search_query))

    order_by = WAREHOUSE_SORT_FIELDS.get(sort_field, 'code')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['code', 'name', 'is_active', 'address']
        headers = ['Code', 'Name', 'Is Active', 'Address']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='warehouses.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='warehouses.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'warehouse/partials/warehouses_list.html', {
            'warehouses': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'warehouses': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
def warehouse_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        code = request.POST.get('code', '').strip()
        address = request.POST.get('address', '').strip()
        is_active = request.POST.get('is_active') == 'on'
        obj = Warehouse(hub_id=hub_id)
        obj.name = name
        obj.code = code
        obj.address = address
        obj.is_active = is_active
        obj.save()
        return _render_warehouses_list(request, hub_id)
    return django_render(request, 'warehouse/partials/panel_warehouse_add.html', {})

@login_required
def warehouse_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(Warehouse, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '').strip()
        obj.code = request.POST.get('code', '').strip()
        obj.address = request.POST.get('address', '').strip()
        obj.is_active = request.POST.get('is_active') == 'on'
        obj.save()
        return _render_warehouses_list(request, hub_id)
    return django_render(request, 'warehouse/partials/panel_warehouse_edit.html', {'obj': obj})

@login_required
@require_POST
def warehouse_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(Warehouse, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_warehouses_list(request, hub_id)

@login_required
@require_POST
def warehouse_toggle_status(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(Warehouse, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_active = not obj.is_active
    obj.save(update_fields=['is_active', 'updated_at'])
    return _render_warehouses_list(request, hub_id)

@login_required
@require_POST
def warehouses_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = Warehouse.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'activate':
        qs.update(is_active=True)
    elif action == 'deactivate':
        qs.update(is_active=False)
    elif action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_warehouses_list(request, hub_id)


# ======================================================================
# StockMovement
# ======================================================================

STOCK_MOVEMENT_SORT_FIELDS = {
    'reference': 'reference',
    'movement_type': 'movement_type',
    'source_zone': 'source_zone',
    'dest_zone': 'dest_zone',
    'status': 'status',
    'quantity': 'quantity',
    'created_at': 'created_at',
}

def _build_stock_movements_context(hub_id, per_page=10):
    qs = StockMovement.objects.filter(hub_id=hub_id, is_deleted=False).order_by('reference')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'stock_movements': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'reference',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_stock_movements_list(request, hub_id, per_page=10):
    ctx = _build_stock_movements_context(hub_id, per_page)
    return django_render(request, 'warehouse/partials/stock_movements_list.html', ctx)

@login_required
@with_module_nav('warehouse', 'warehouses')
@htmx_view('warehouse/pages/stock_movements.html', 'warehouse/partials/stock_movements_content.html')
def stock_movements_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'reference')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = StockMovement.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(reference__icontains=search_query) | Q(movement_type__icontains=search_query) | Q(notes__icontains=search_query) | Q(status__icontains=search_query))

    order_by = STOCK_MOVEMENT_SORT_FIELDS.get(sort_field, 'reference')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['reference', 'movement_type', 'source_zone', 'dest_zone', 'status', 'quantity']
        headers = ['Reference', 'Movement Type', 'Zone', 'Zone', 'Status', 'Quantity']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='stock_movements.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='stock_movements.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'warehouse/partials/stock_movements_list.html', {
            'stock_movements': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'stock_movements': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
def stock_movement_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        reference = request.POST.get('reference', '').strip()
        movement_type = request.POST.get('movement_type', '').strip()
        quantity = request.POST.get('quantity', '0') or '0'
        notes = request.POST.get('notes', '').strip()
        status = request.POST.get('status', '').strip()
        obj = StockMovement(hub_id=hub_id)
        obj.reference = reference
        obj.movement_type = movement_type
        obj.quantity = quantity
        obj.notes = notes
        obj.status = status
        obj.save()
        return _render_stock_movements_list(request, hub_id)
    return django_render(request, 'warehouse/partials/panel_stock_movement_add.html', {})

@login_required
def stock_movement_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(StockMovement, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.reference = request.POST.get('reference', '').strip()
        obj.movement_type = request.POST.get('movement_type', '').strip()
        obj.quantity = request.POST.get('quantity', '0') or '0'
        obj.notes = request.POST.get('notes', '').strip()
        obj.status = request.POST.get('status', '').strip()
        obj.save()
        return _render_stock_movements_list(request, hub_id)
    return django_render(request, 'warehouse/partials/panel_stock_movement_edit.html', {'obj': obj})

@login_required
@require_POST
def stock_movement_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(StockMovement, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_stock_movements_list(request, hub_id)

@login_required
@require_POST
def stock_movements_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = StockMovement.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_stock_movements_list(request, hub_id)


@login_required
@permission_required('warehouse.manage_settings')
@with_module_nav('warehouse', 'settings')
@htmx_view('warehouse/pages/settings.html', 'warehouse/partials/settings_content.html')
def settings_view(request):
    return {}

