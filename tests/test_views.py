"""Tests for warehouse views."""
import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestDashboard:
    """Dashboard view tests."""

    def test_dashboard_loads(self, auth_client):
        """Test dashboard page loads."""
        url = reverse('warehouse:dashboard')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_dashboard_htmx(self, auth_client):
        """Test dashboard HTMX partial."""
        url = reverse('warehouse:dashboard')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_dashboard_requires_auth(self, client):
        """Test dashboard requires authentication."""
        url = reverse('warehouse:dashboard')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestWarehouseViews:
    """Warehouse view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('warehouse:warehouses_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('warehouse:warehouses_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('warehouse:warehouses_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('warehouse:warehouses_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('warehouse:warehouses_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('warehouse:warehouses_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('warehouse:warehouse_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('warehouse:warehouse_add')
        data = {
            'name': 'New Name',
            'code': 'New Code',
            'address': 'Test description',
            'is_active': 'on',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, warehouse):
        """Test edit form loads."""
        url = reverse('warehouse:warehouse_edit', args=[warehouse.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, warehouse):
        """Test editing via POST."""
        url = reverse('warehouse:warehouse_edit', args=[warehouse.pk])
        data = {
            'name': 'Updated Name',
            'code': 'Updated Code',
            'address': 'Test description',
            'is_active': '',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, warehouse):
        """Test soft delete via POST."""
        url = reverse('warehouse:warehouse_delete', args=[warehouse.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        warehouse.refresh_from_db()
        assert warehouse.is_deleted is True

    def test_toggle_status(self, auth_client, warehouse):
        """Test toggle active status."""
        url = reverse('warehouse:warehouse_toggle_status', args=[warehouse.pk])
        original = warehouse.is_active
        response = auth_client.post(url)
        assert response.status_code == 200
        warehouse.refresh_from_db()
        assert warehouse.is_active != original

    def test_bulk_delete(self, auth_client, warehouse):
        """Test bulk delete."""
        url = reverse('warehouse:warehouses_bulk_action')
        response = auth_client.post(url, {'ids': str(warehouse.pk), 'action': 'delete'})
        assert response.status_code == 200
        warehouse.refresh_from_db()
        assert warehouse.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('warehouse:warehouses_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestStockMovementViews:
    """StockMovement view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('warehouse:stock_movements_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('warehouse:stock_movements_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('warehouse:stock_movements_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('warehouse:stock_movements_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('warehouse:stock_movements_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('warehouse:stock_movements_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('warehouse:stock_movement_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('warehouse:stock_movement_add')
        data = {
            'reference': 'New Reference',
            'movement_type': 'New Movement Type',
            'quantity': '100.00',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, stock_movement):
        """Test edit form loads."""
        url = reverse('warehouse:stock_movement_edit', args=[stock_movement.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, stock_movement):
        """Test editing via POST."""
        url = reverse('warehouse:stock_movement_edit', args=[stock_movement.pk])
        data = {
            'reference': 'Updated Reference',
            'movement_type': 'Updated Movement Type',
            'quantity': '100.00',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, stock_movement):
        """Test soft delete via POST."""
        url = reverse('warehouse:stock_movement_delete', args=[stock_movement.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        stock_movement.refresh_from_db()
        assert stock_movement.is_deleted is True

    def test_bulk_delete(self, auth_client, stock_movement):
        """Test bulk delete."""
        url = reverse('warehouse:stock_movements_bulk_action')
        response = auth_client.post(url, {'ids': str(stock_movement.pk), 'action': 'delete'})
        assert response.status_code == 200
        stock_movement.refresh_from_db()
        assert stock_movement.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('warehouse:stock_movements_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestSettings:
    """Settings view tests."""

    def test_settings_loads(self, auth_client):
        """Test settings page loads."""
        url = reverse('warehouse:settings')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_settings_requires_auth(self, client):
        """Test settings requires authentication."""
        url = reverse('warehouse:settings')
        response = client.get(url)
        assert response.status_code == 302

