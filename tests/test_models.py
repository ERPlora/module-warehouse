"""Tests for warehouse models."""
import pytest
from django.utils import timezone

from warehouse.models import Warehouse, StockMovement


@pytest.mark.django_db
class TestWarehouse:
    """Warehouse model tests."""

    def test_create(self, warehouse):
        """Test Warehouse creation."""
        assert warehouse.pk is not None
        assert warehouse.is_deleted is False

    def test_str(self, warehouse):
        """Test string representation."""
        assert str(warehouse) is not None
        assert len(str(warehouse)) > 0

    def test_soft_delete(self, warehouse):
        """Test soft delete."""
        pk = warehouse.pk
        warehouse.is_deleted = True
        warehouse.deleted_at = timezone.now()
        warehouse.save()
        assert not Warehouse.objects.filter(pk=pk).exists()
        assert Warehouse.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, warehouse):
        """Test default queryset excludes deleted."""
        warehouse.is_deleted = True
        warehouse.deleted_at = timezone.now()
        warehouse.save()
        assert Warehouse.objects.filter(hub_id=hub_id).count() == 0

    def test_toggle_active(self, warehouse):
        """Test toggling is_active."""
        original = warehouse.is_active
        warehouse.is_active = not original
        warehouse.save()
        warehouse.refresh_from_db()
        assert warehouse.is_active != original


@pytest.mark.django_db
class TestStockMovement:
    """StockMovement model tests."""

    def test_create(self, stock_movement):
        """Test StockMovement creation."""
        assert stock_movement.pk is not None
        assert stock_movement.is_deleted is False

    def test_str(self, stock_movement):
        """Test string representation."""
        assert str(stock_movement) is not None
        assert len(str(stock_movement)) > 0

    def test_soft_delete(self, stock_movement):
        """Test soft delete."""
        pk = stock_movement.pk
        stock_movement.is_deleted = True
        stock_movement.deleted_at = timezone.now()
        stock_movement.save()
        assert not StockMovement.objects.filter(pk=pk).exists()
        assert StockMovement.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, stock_movement):
        """Test default queryset excludes deleted."""
        stock_movement.is_deleted = True
        stock_movement.deleted_at = timezone.now()
        stock_movement.save()
        assert StockMovement.objects.filter(hub_id=hub_id).count() == 0


