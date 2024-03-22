from dataclasses import dataclass
from rest_framework import serializers

from order.models import Address, Order, OrderItem
from shipment.serializers import ShipmentSerializer

default_errors = {
    'invalid_string': "Incorrect type: Expected a string but got {input_type}",
    'empty_field': "Got an empty value",
    'invalid_currency': "string did not start with a valid currency: {valid_currencies}",
    'invalid_price': "price data did not convert to a float: {data}",
}

@dataclass
class Currency:
    currency: str
    price: float


class CurrencyAmountField(serializers.Field):
    def to_representation(self, value):
        return f"{OrderItem.CURRENCY_SYMBOLS[value.currency]}{value.price}"
    
    @classmethod
    def to_internal_value(data):
        valid_symbols = list(OrderItem.SYMBOL_CURRENCIES.keys())
        
        if not isinstance(data, str):
            self.fail('incorrect_type', input_type=type(data).__name__)
        if not data:
            self.fail('empty_field')
        currency = data[0]
        if not currency in valid_symbols:
            self.fail('invalid_currency', valid_currencies=valid_symbols)
        try:
            price = float(data[1:])
        except ValueError:
            self.fail('invalid_price', data=data[1:])
        raise Exception("I was here", currency, price, data)
        return {
            'currency': currency,
            'price': price
        }

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
    uuid = serializers.UUIDField(read_only=True)
    sku = serializers.CharField(max_length=255)
    amount = CurrencyAmountField(source='*')
    currency = serializers.CharField(max_length=255)
    price = serializers.IntegerField()
    quantity = serializers.IntegerField()

    def to_internal_value(self, data):
        if 'amount' in data:
            data.update(CurrencyAmountField.to_internal_value(data['amount']))
        return super().to_internal_value(data)
            

    class Meta:
        model = OrderItem
        fields = ('amount', 'sku', 'uuid', 'quantity', 'price', 'currency')


class OrderSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    order_items = OrderItemSerializer(many=True)
    shipments = ShipmentSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        # fields = ('order_number', 'ordered_at', 'customer_address', 'items')
