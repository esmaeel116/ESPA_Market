from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderItemViewSet, confirm_payment, order_invoice, simulate_payment

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'order-items', OrderItemViewSet, basename='order-items')

urlpatterns = [
    path('', include(router.urls)),
    path('confirm-payment/', confirm_payment, name='confirm-payment'),
    path('orders/<int:order_id>/invoice/', order_invoice, name='order-invoice'),
    path('orders/simulate-payment/', simulate_payment, name='simulate-payment'),
]
