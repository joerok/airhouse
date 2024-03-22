from rest_framework.test import APITestCase
import pdb


class OrderViewSetTestCase(APITestCase):
    def test_order_view_set_list(self):
        response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code, 200)

    def test_order_create_fake_order(self):
        response = self.client.get('/api/orders/?fake_order')
        data = response.json()
        self.assertEqual(response.status_code, 200)

    def test_order_item_update_amount_changes_price_and_currency(self):
        response = self.client.get('/api/orders/?fake_order')
        order_id = response.json()['uuid']
        response = self.client.get(f'/api/orders/{order_id}/', context_type="application/json")
        order_item_id = data['order_items'][0]['uuid']
        order_item = data['order_items'][0]
        order_item.update(
            amount='€6000.00'
        )
        del order_item['price']
        del order_item['currency']
        response = self.client.put(f'/api/order_items/{order_item_id}/', order_item, format='json')
        self.assertTrue(response.status_code, 201)
        response = self.client.put(f'/api/order_items/{order_item_id}/', order_item, format='json')
        order_item = response.json()
        self.assertEqual(order_item['amount'], '€6000.00')
        self.assertEqual(order_item['price'], 6000.00)
        self.assertEqual(order_item['currency'], '€')


    def test_order_item_update_price_and_currency_changes_amount(self):
        response = self.client.get('/api/orders/?fake_order')
        order_id = response.json()['uuid']
        response = self.client.get(f'/api/orders/{order_id}/', context_type="application/json")
        order_item_id = data['order_items'][0]['uuid']
        order_item = data['order_items'][0]
        order_item.update(
            currency='€',
            price='7000'
        )
        del order_item['amount']
        response = self.client.put(f'/api/order_items/{order_item_id}/', order_item, format='json')
        self.assertTrue(response.status_code, 201)
        response = self.client.put(f'/api/order_items/{order_item_id}/', order_item, format='json')
        order_item = response.json()
        self.assertEqual(order_item['amount'], '€7000.00')
        self.assertEqual(order_item['price'], 7000.00)
        self.assertEqual(order_item['currency'], '€')
