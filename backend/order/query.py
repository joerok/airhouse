from django.db import models
from django.db.models.functions import Coalesce

class OrderQueryManager(models.Manager):
    def get_queryset(self):
        return OrderQuerySet(model=self.model, using=self._db, hints=self._hints)
    
    def get_totals(self, order=None):
        return self.get_queryset().get_totals(order=order)

    def expensive(self, min_price=100):
        return self.filter(total_price__gt=min_price)

    def split_ship(self):
        return self.filter(shipments__gt=1)

    def split_line(self):
        return self.filter(order_items__shipment_items__gt=1)


class OrderQuerySet(models.QuerySet):
    def get_totals(self, order=None):
        return (
            order.order_items.annotate(
                total_line_price=models.F('quantity') * models.F('price'),
                line_quantity_shipped=models.F('shipment_items__quantity'),
            ).aggregate(
                total_quantity=Coalesce(models.Sum('quantity'), 0),
                total_price=Coalesce(models.Sum('total_line_price'), float(0)),
                quantity_shipped=Coalesce(models.Sum('line_quantity_shipped'), 0),
            )
        )
