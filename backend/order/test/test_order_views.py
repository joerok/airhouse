from rest_framework.test import APITestCase


class OrderViewSetTestCase(APITestCase):
    def test_order_view_set_list(self):
        response = self.client.get('/api/orders/')
        raise Exception(resposne.data)
        self.assertEqual(response.status_code, 200)
