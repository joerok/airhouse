from uuid import uuid4

from django.db import models

from order.query import OrderQuerySet


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

    @property
    def total_order_price(self):
        """ * total order price (sum of item price) """
        try:
            self.order_items.with_total_price().total_price
        except e:
            raise Exception(e)

    @property
    def quantity_ordered(self):
        """ * total number of items ordered (sum of item quantity) """
        return self.total_order_price()

    @property
    def number_of_shipments(self):
        """ * total number of shipments (count of shipments) """
        return len(self.shipments.all())

    __shipped_item_counts = None
    def update_shipped_item_counts(self):
        if not self.__shipped_item_counts:
            annotation = self.order_items.annotate(
                items_shipped=models.Sum('shipment_items__quantity')
            ).aggregate(
                total_items_ordered=models.Sum('quantity'),
                total_items_shipped=models.Sum('items_shipped')
            )
            items_with_shipments = (annotation.get('total_items_shipped') or 0)
            items_without_shipments = (annotation.get('total_items_ordered') or 0) - items_with_shipments

            self.__shipped_item_counts = dict(
                shipped=items_with_shipments,
                unshipped=items_without_shipments,
            )

    def reset_shipped_item_counts(self):
        self.__shipped_item_counts = None

    @property
    def unshipped_items_count(self):
        self.update_shipped_item_counts()
        return self.__shipped_item_counts['unshipped']

    @property
    def shipped_items_count(self):
        """ * total number of items shipped (sum of item quantity in shipments """
        self.update_shipped_item_counts()
        return self.__shipped_item_counts['shipped']

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
