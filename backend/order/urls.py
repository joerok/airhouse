from rest_framework.routers import DefaultRouter

from order.views import OrderViewSet, OrderItemViewSet


router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'orders/<int:order_id>/items', OrderItemViewSet, basename='order_item')
urlpatterns = router.urls
