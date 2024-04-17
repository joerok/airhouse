from uuid import uuid4

from django.db import models

from order.query import OrderQuerySet, OrderItemQuerySet


class Address(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255, blank=True)


class Order(models.Model):
    STATUS_OPEN = 'open'
    STATUS_PARTIAL = 'partial'
    STATUS_CLOSED = 'closed'
    STATUS_CHOICES = [
        (STATUS_OPEN, 'Open'),
        (STATUS_PARTIAL, 'Partial'),
        (STATUS_CLOSED, 'Closed'),
    ]

    objects = OrderQuerySet.as_manager()

    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    order_number = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default=STATUS_OPEN)
    ordered_at = models.DateTimeField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cached_totals = None

    def get_totals(self):
        if self._cached_totals is None:
            # Calculate totals if not cached
            item_totals = Order.objects.get_totals(order=self)
            self._cached_totals = {
                'total_price': item_totals['total_price'],
                'total_quantity': item_totals['total_quantity'],
                'quantity_shipped': item_totals['quantity_shipped'],
                'quantity_unshipped': item_totals['total_quantity'] - item_totals['quantity_shipped']
            }

        return self._cached_totals

    @property
    def total_order_price(self):
        """ * total order price (sum of item price) """
        return self.get_totals()['total_price']

    @property
    def quantity_ordered(self):
        """ * total number of items ordered (sum of item quantity) """

        return self.get_totals()['total_quantity']
    
    @property
    def number_of_shipments(self):
        """ * total number of shipments (count of shipments) """
        return self.shipments.count()

    @property
    def unshipped_items_count(self):
        return self.get_totals()['quantity_unshipped']

    @property
    def shipped_items_count(self):
        """ * total number of items shipped (sum of item quantity in shipments """
        return self.get_totals()['quantity_shipped']

    class Meta:
        ordering = ['ordered_at']


class OrderItem(models.Model):
    CURRENCY_USD = 'USD'
    CURRENCY_GBP = 'GBP'
    CURRENCY_EUR = 'EUR'
    CURRENCY_CHOICES = [
        (CURRENCY_USD, '$ (USD)'),
        (CURRENCY_GBP, '£ (GBP)'),
        (CURRENCY_EUR, '€ (EUR)'),
    ]
    CURRENCY_SYMBOLS = {
        CURRENCY_USD: '$',
        CURRENCY_GBP: '£',
        CURRENCY_EUR: '€',
    }
    SYMBOL_CURRENCIES = dict((s,c) for c,s in CURRENCY_SYMBOLS.items())

    objects = OrderItemQuerySet.as_manager()


    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    sku = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=16, default=CURRENCY_USD)
