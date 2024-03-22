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
        response = self.client.get('/api/orders/?fake_order')
        order_id = response.json()['uuid']
        response = self.client.get(f'/api/orders/{order_id}/', context_type="application/json")
        try:
            data = response.json()
        except:
            raise Exception(response)
        order_item_id = data['order_items'][0]['uuid']
        raise Exception(self.client.patch(f'/api/order_items/{order_item_id}/', {"price": 5000, 'currency': 'EUR'}, content_type='application/json'))
        response = self.client.get(f'/api/orders/{order_id}/', context_type="application/json")
        raise Exception(response.json())
        self.assertEqual(items[0]['amount'], '$100.00')
