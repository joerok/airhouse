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
        items = data['order']['order_items']
        raise Exception(data)
        self.assertEqual(items[0]['amount'], '$100.00')
