from dataclasses import dataclass
from rest_framework import serializers

from order.models import Address, Order, OrderItem
from shipment.serializers import ShipmentSerializer
from backend.common.match import match


@dataclass
class Currency:
    currency: str
    price: float


class CurrencyAmountField(serializers.Field):
    default_error_messages = {
        'incorrect_type': "Incorrect type: Expected a string but got {input_type}",
        'empty_field': "Got an empty value",
        'invalid_currency_symbol': "string did not start with a valid currency: {valid_currencies}",
        'invalid_price': "price data did not convert to a float: {data}",
    }

    def to_representation(self, value):
        return f"{OrderItem.CURRENCY_SYMBOLS[value.currency]}{value.price}"
    
    def to_internal_value(self, data):
        valid_symbols = list(OrderItem.SYMBOL_CURRENCIES.keys())
        
        if not isinstance(data, str):
            self.fail('incorrect_type', input_type=type(data).__name__)
        if not data:
            self.fail('empty_field')
        symbol = data[0]
        if not symbol in valid_symbols:
            self.fail('invalid_currency_symbol', valid_currencies=valid_symbols)
        currency = OrderItem.SYMBOL_CURRENCIES[symbol]
        try:
            price = float(data[1:])
        except ValueError:
            self.fail('invalid_price', data=data[1:])

        return {
            'currency': currency,
            'price': price
        }

class AddressSerializer(serializers.Serializer):
    default_error_messages = {
        'invalid_phone_number': 'Order number must be in the format (xxx) xxx-xxxx: {value}',
    }

    address_line_1 = serializers.CharField(max_length=255)
    address_line_2 = serializers.CharField(max_length=255, required=False)
    city = serializers.CharField(max_length=255)
    state = serializers.CharField(max_length=255)
    postal_code = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(max_length=255, required=False)

    def validate_phone_number(self, value):
        """     * phone number should follow the convention `(xxx) xxx-xxxx` (just focus on structure, we can't support digits yet) """
        if not match("(...) ...-....", value):
            raise self.fail("invalid_phone_number", value=value)
        return value

    class Meta:
        model = Address
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    sku = serializers.CharField(max_length=255)
    amount = CurrencyAmountField(source='*', required=False)
    currency = serializers.CharField(max_length=255, required=False)
    price = serializers.DecimalField(required=False, max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField()

    class Meta:
        model = OrderItem
        fields = ('amount', 'sku', 'uuid', 'quantity', 'price', 'currency')


class OrderSerializer(serializers.ModelSerializer):
    default_error_messages = {
        'invalid_order_number': 'Order number must begin with `ORD#` followed by at least four characters: {value}',
    }

    address = AddressSerializer()
    order_items = OrderItemSerializer(many=True)
    shipments = ShipmentSerializer(many=True, read_only=True)
    total_order_price = serializers.DecimalField(required=False, read_only=True, max_digits=10, decimal_places=2)
    quantity_ordered = serializers.IntegerField(required=False, read_only=True)
    number_of_shipments = serializers.IntegerField(required=False, read_only=True)
    shipped_items_count = serializers.IntegerField(required=False, read_only=True)

    def validate_order_number(self, value):
        """    * order numbers should all begin with `ORD#` followed by at least four characters"""
        if not match("ORD#....+", value):
            raise self.fail("invalid_order_number", value=value)
        return value
        
    class Meta:
        model = Order
        fields = '__all__'
        # fields = ('order_number', 'ordered_at', 'customer_address', 'items')
