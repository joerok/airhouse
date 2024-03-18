from rest_framework import serializers

from order.models import Address, Order, OrderItem
from shipment.serializers import ShipmentSerializer


class AddressSerializer(serializers.Serializer):
    address_line_1 = serializers.CharField(max_length=255)
    address_line_2 = serializers.CharField(max_length=255, required=False)
    city = serializers.CharField(max_length=255)
    state = serializers.CharField(max_length=255)
    postal_code = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = Address
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    order_items = OrderItemSerializer(many=True)
    shipments = ShipmentSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        # fields = ('order_number', 'ordered_at', 'customer_address', 'items')
