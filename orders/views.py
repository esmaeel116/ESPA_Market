from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.select_related('customer')\
            .prefetch_related('items__product')\
            .filter(customer__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer)


class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderItem.objects.select_related('order', 'product')\
            .filter(order__customer__user=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirm_payment(request):
    order_id = request.data.get('order_id')

    if not order_id:
        return Response({'detail': 'Order ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        order = Order.objects.get(id=order_id, customer__user=request.user)
    except Order.DoesNotExist:
        return Response({'detail': 'Order not found or access denied.'}, status=status.HTTP_404_NOT_FOUND)

    if order.is_paid:
        return Response({'detail': 'This order is already paid.'}, status=status.HTTP_400_BAD_REQUEST)

    order.is_paid = True
    order.status = 'completed'
    order.save()

    return Response({'detail': f'Order #{order.id} marked as paid.'}, status=status.HTTP_200_OK)