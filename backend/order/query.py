from django.db import models


class OrderQueryManager(models.Manager):
    def get_queryset(self):
        return OrderQuerySet(model=self.model, using=self._db, hints=self._hints)
    
    def expensive(self, min_price=100):
        return self.get_queryset().with_total_price().filter(total_price__gt=min_price)

    def split_ship(self):
        return self.filter(shipments__gt=1)

    def split_line(self):
        return self.filter(order_items__shipment_items__gt=1)


class OrderQuerySet(models.QuerySet):
    def with_total_price(self):
        return self.annotate(total_price=model.Sum('items__price' * 'items__orderitem__quantity'))


class OrderItemQueryManager(models.Manager):
    def get_queryset(self):
        return OrderItemQuerySet(model=self.model, using=self._db, hints=self._hints)


class OrderItemQuerySet(models.QuerySet):
    def with_total_price(self):
        return self.annotate(total_price=model.Sum('price' * 'quantity'))
