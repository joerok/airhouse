from django.db import models
from django.db.models.functions import Coalesce
from decimal import Decimal

class OrderQueryManager(models.Manager):
    def get_queryset(self):
        return OrderQuerySet(model=self.model, using=self._db, hints=self._hints)
    
    def get_totals(self, order=None):
        return self.get_queryset().with_totals()

    def expensive(self, min_price=100):
        return self.get_queryset().with_totals().filter(total_price__gt=min_price)

    def split_ship(self):
        return self.filter(shipments__gt=1)

    def split_line(self):
        return self.filter(order_items__shipment_items__gt=1)


class OrderQuerySet(models.QuerySet):
    def with_totals(self):
        return (
            self.annotate(
                total_line_price=models.F('order_items__quantity') * models.F('order_items__price'),
                line_quantity_shipped=models.F('order_items__shipment_items__quantity'),
            ).aggregate(
                total_quantity=Coalesce(models.Sum('order_items__quantity'), 0),
                total_price=Coalesce(models.Sum('total_line_price'), Decimal(0)),
                quantity_shipped=Coalesce(models.Sum('line_quantity_shipped'), 0),
            )
        )
