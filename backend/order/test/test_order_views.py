from rest_framework.test import APITestCase
from rest_framework.exceptions import ValidationError
from order.test.factory import OrderFactory
from shipment.test.factory import ShipmentFactory
from order.serializers import OrderSerializer, OrderItemSerializer


class OrderViewSetTestCase(APITestCase):
    def setUp(self):
        from django.conf import settings
        from django.db import connection, reset_queries
        settings.DEBUG = True
        reset_queries()

    def tearDown(self):
        from django.conf import settings
        from django.db import connection, reset_queries
        #raise Exception(list(filter(lambda x: not(x.startswith("INSERT") or x.startswith("UPDATE")), map(lambda x: x['sql'][:50], connection.queries))))

        settings.DEBUG = False    


    def test_order_view_set_list(self):
        response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code, 200)

    def test_order_create_fake_order(self):
        response = self.client.get('/api/orders/?fake_order')
        self.assertEqual(response.status_code, 201)

    def test_order_total_price(self):
        fake_order = OrderFactory()
        serializer = OrderSerializer(instance=fake_order)
        self.assertTrue(float(serializer.data['total_order_price']) > 0, serializer.data)

    def test_order_quantity_ordered(self):
        fake_order = OrderFactory()
        serializer = OrderSerializer(instance=fake_order)
        self.assertTrue(serializer.data['quantity_ordered'] > 0)

    def test_total_shipments(self):
        fake_order = OrderFactory()
        fake_shipment = ShipmentFactory(order=fake_order)
        serializer = OrderSerializer(instance=fake_order)
        self.assertTrue(serializer.data['number_of_shipments'] > 0)

    def test_items_shipped(self):
        fake_order = OrderFactory()
        fake_shipment = ShipmentFactory(order=fake_order)
        serializer = OrderSerializer(instance=fake_order)
        self.assertTrue(serializer.data['shipped_items_count'] > 0)

    def test_order_item_update_amount_changes_price_and_currency(self):
        fake_order = OrderFactory()
        serializer = OrderItemSerializer(instance=fake_order.order_items.first(), data={'amount':'€6000.12'}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.assertEqual(serializer.data['amount'], '€6000.12')
        self.assertEqual(serializer.data['price'], '6000.12')
        self.assertEqual(serializer.data['currency'], 'EUR')

    def test_order_item_update_price_and_currency_changes_amount(self):
        fake_order = OrderFactory()
        serializer = OrderItemSerializer(
            instance=fake_order.order_items.first(), 
            data={'currency':'EUR', 'price':'7000.98'},
            partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.assertEqual(serializer.data['amount'], '€7000.98')
        self.assertEqual(serializer.data['price'], '7000.98')
        self.assertEqual(serializer.data['currency'], 'EUR')

    def test_order_item_update_amount_bad_currency(self):
        fake_order = OrderFactory()
        serializer = OrderItemSerializer(
            instance=fake_order.order_items.first(), 
            data={'amount':'M7000.98'},
            partial=True)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_order_item_update_amount_bad_type(self):
        fake_order = OrderFactory()
        serializer = OrderItemSerializer(
            instance=fake_order.order_items.first(), 
            data={'amount': 1},
            partial=True)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_order_item_update_amount_empty_data(self):
        fake_order = OrderFactory()
        serializer = OrderItemSerializer(
            instance=fake_order.order_items.first(), 
            data={'amount': ""},
            partial=True)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_order_item_update_amount_bad_amount(self):
        fake_order = OrderFactory()
        serializer = OrderItemSerializer(
            instance=fake_order.order_items.first(), 
            data={'amount':'MNOMONEY'},
            partial=True)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_order_bad_number(self):
        fake_order = OrderFactory()
        with self.assertRaises(ValidationError):
            serializer = OrderSerializer(instance=fake_order, data={'order_number':'ORD#123'}, partial=True)
            serializer.is_valid(raise_exception=True)

    def test_expensive_order(self):
        fake_order = OrderFactory()
        Order.objects.expensive(fake_order)