from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from django.db.models.signals import post_save

from order.models import Order, OrderItem
from order.serializers import OrderSerializer, OrderItemSerializer
from shipment.models import ShipmentItem

def update_order_status_from_shipment_items(sender, instance, created, **kwargs):
    if created:
        order = instance.order_item.order
        if order.status in (Order.STATUS_OPEN, Order.STATUS_PARTIAL):
            if order.unshipped_items_count == 0:
                order.status = Order.STATUS_CLOSED
            elif order.shipped_items_count > 0:
                order.status = Order.STATUS_PARTIAL

post_save.connect(update_order_status_from_shipment_items, sender=ShipmentItem)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def create_fake_order(self):  # request, *args, **kwargs):
        from order.test.factory import OrderFactory
        fake_order = OrderFactory()
        serializer = self.get_serializer(instance=fake_order)
        headers = self.get_success_headers(serializer.data)
        print(f'Created fake order: {fake_order}')
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)

    def create_fake_shipment(self):
        from shipment.test.factory import ShipmentFactory
        order = self.get_object()
        fake_shipment = ShipmentFactory(order=order)
        serializer = self.get_serializer(instance=order)
        headers = self.get_success_headers(serializer.data)
        print(f'Created fake shipment: {fake_shipment}')
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        if 'fake_order' in request.query_params:
            return self.create_fake_order()

        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if 'fake_shipment' in request.query_params:
            return self.create_fake_shipment()
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, pk=None):
        order = self.get_object()
        serializer = self.serializer_class(order, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()

    def update(self, request, pk=None):
        order_item = self.get_object()
        serializer = self.serializer_class(order_item, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
