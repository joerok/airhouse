from uuid import uuid4

from django.db import models


class Shipment(models.Model):
    order = models.ForeignKey('order.Order', on_delete=models.CASCADE, related_name='shipments')
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    shipped_at = models.DateTimeField()
    method = models.CharField(max_length=255)
    tracking_number = models.CharField(max_length=255)


class ShipmentItem(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='shipment_items')
    order_item = models.ForeignKey('order.OrderItem', on_delete=models.CASCADE, related_name='shipment_items')
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    quantity = models.IntegerField()
