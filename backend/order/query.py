from django.db import models


class OrderQueryManager(models.Manager):
    def get_queryset(self):
        return OrderQuerySet(model=self.model, using=self._db, hints=self._hints)
    
    def get_totals(self, pk=None):
        return self.get_queryset().get_totals(pk=pk)

    def expensive(self, min_price=100):
        return self.get_totals().filter(total_price__gt=min_price)

    def split_ship(self):
        return self.filter(shipments__gt=1)

    def split_line(self):
        return self.filter(order_items__shipment_items__gt=1)


class OrderQuerySet(models.QuerySet):
    def get_totals(self, pk=None):
        return (
            self.get(pk=pk).annotate(
                    total_price=models.F('order_items__quantity') * models.F('order_items__price'),
                    quantity_shipped=models.F('order_items__shipment_items__quantity'),
                )
                .aggregate(
                    total_quantity=models.Sum('quantity'),
                    total_price=models.Sum('total_price'),
                    quantity_shipped=models.Sum('quantity_shipped'),
                )
        )


class OrderItemQuerySet(models.QuerySet):
    def with_total_price(self):
        return self.annotate(total_price=models.Sum(models.F('price') * models.F('quantity')))

    def with_quantity_ordered(self):
        return self.annotate(quantity_ordered=models.Sum(models.F('quantity')))
