from rest_framework.test import APITestCase


class OrderViewSetTestCase(APITestCase):
    def test_order_view_set_list(self):
        response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code, 200)

    def test_order_create_fake_order(self):
        response = self.client.get('/api/orders/?fake_order')
        data = response.json()
        raise Exception(data)
        self.assertEqual(response.status_code, 200)

    def test_order_item_patch(self):
        response = self.client.get('/api/orders/')
        data = response.json()
        order_item_id = data['order_items'][0]['uuid']
        raise Exception(self.client.patch(f'/api/order_item/{order_item_id}', {"price": 5000, 'currency': 'EUR'}))
        raise Exception(data)
        self.assertEqual(items[0]['amount'], '$100.00')
