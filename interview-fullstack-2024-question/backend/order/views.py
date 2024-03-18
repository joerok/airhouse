from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from order.models import Order
from order.serializers import OrderSerializer


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
