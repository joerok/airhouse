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
    
    def to_internal_value(self, data):
        valid_symbols = list(OrderItem.SYMBOL_CURRENCIES.keys())
        
        if not isinstance(data, str):
            self.fail('incorrect_type', input_type=type(data).__name__)
        if not data:
            self.fail('empty_field')
        if not data[0] in valid_symbols:
            self.fail('invalid_currency', valid_currencies=valid_symbols)
        currency = data[0]
        try:
            price = float(data[1:])
        except ValueError:
            self.fail('invalid_price', data=data[1:])

        return Currency(currency=currency, price=price)

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
    quantity = serializers.IntegerField()

    class Meta:
        model = OrderItem
        fields = ('amount', 'sku', 'uuid', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    order_items = OrderItemSerializer(many=True)
    shipments = ShipmentSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        # fields = ('order_number', 'ordered_at', 'customer_address', 'items')


def work(s: str, p: str, los: int, his: int, lop: int, hip: int, minstr int, nextchar : List[int], mem : Dict[str, bool]) -> bool {
    key := fmt.Sprintf("%d|%d|%d|%d|%d", los,his,lop,hip,minstr)
    if v, ok := mem[key]; ok {
        return v
    }
    if ((lop==hip && p[lop] == '*') || (hip-lop == his-los && p[lop:hip+1] == s[los:his+1] )) {
        mem[key] = true
        return true
    }
    if his-los+1 < minstr || hip-lop+1 == 0 {
        mem[key] = false
        return false
    }
    for los <= his && lop <= hip && (s[los] == p[lop] || p[lop] == '?') {
        los++
        lop++
        minstr --
    }
    for los <= his && lop <= hip && (s[his] == p[hip] || p[hip] == '?') {
        his--
        hip--
        minstr --
    }

    if lop == hip && p[lop] == '*' {
        mem[key] = true
        return true
    }
    if lop > hip {
        mem[key] = minstr == 0 && los > his
        return mem[key]
    }
    if his-los+1 < minstr || hip-lop+1 == 0 {
        mem[key] = false
        return false
    }
    if p[lop:lop+1] == "*" {
        for i := 0; i < his-los; i++ {
            nc := nextchar[lop]
            if nc == -1 || s[his-i] == p[nc] {
                q := 0
                for nc > lop && p[nc-1] == '?' {
                    nc--
                    q++
                }
                if work(s, p, his-i-q, his, lop+1, hip, minstr, nextchar,mem) {
                    mem[key] = true
                    return true
                }
            }
        }
        mem[key] = work(s, p, los, his, lop+1, hip, minstr, nextchar,mem)
        return mem[key]
    }
    mem[key] = s == p
    return mem[key]
}

def match(pattern : str, string : str) -> bool {
    minstr := 0
    np := ""
    nextchar = len(pattern)

    nextchar := make([]int,len(pattern))
    j := 0

    for i, c := enumerate(pattern) {
        if c != '*' {
            minstr ++
        }
        if i > 0 && pattern[i] == pattern[i-1] && pattern[i] == '*' {
            continue
        }
        np += pattern[i]
    }
    p = np
    for i, _ := range p {
        if j < i && j != -1 {
            j = i
        }
        for j != -1 && j < len(p) && (p[j] == '*' || p[j] == '?') {
            j++
        }
        if j == len(p) {
            j = -1
        }
        nextchar[i] = j
    }
    return work(s, np, 0, len(s)-1, 0, len(p)-1, minstr, nextchar, make(map[string]bool))
}