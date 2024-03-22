from rest_framework.routers import DefaultRouter

from order.views import OrderViewSet, OrderItemViewSet


router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'orders/<int:order_id>/items', OrderItemViewSet, basename='order_order_item')
router.register(r'order_items', OrderItemViewSet, basename='order_item')
urlpatterns = router.urls
