from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import get_template

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.select_related('customer') \
            .prefetch_related('items__product') \
            .filter(customer__user=self.request.user, is_paid=True)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer)


class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderItem.objects.select_related('order', 'product') \
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_invoice(request, order_id):
    try:
        order = Order.objects.select_related('customer__user') \
            .prefetch_related('items__product') \
            .get(id=order_id, customer__user=request.user, is_paid=True)
    except Order.DoesNotExist:
        return Response({'detail': 'Order not found or not paid.'}, status=status.HTTP_404_NOT_FOUND)

    template = get_template('orders/invoice.html')
    html = template.render({'order': order})

    result = BytesIO()
    pisa_status = pisa.CreatePDF(src=html, dest=result)

    if pisa_status.err:
        return Response({'detail': 'PDF generation failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    response = HttpResponse(result.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=invoice_order_{order.id}.pdf'
    return response


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def simulate_payment(request):
    order_id = request.data.get('order_id')

    try:
        order = Order.objects.get(id=order_id, customer__user=request.user)
    except Order.DoesNotExist:
        return Response({'detail': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

    if order.is_paid:
        return Response({'detail': 'Order already paid.'}, status=status.HTTP_400_BAD_REQUEST)

    order.is_paid = True
    order.status = 'processing'
    order.save()

    return Response({'detail': f'Payment successful for Order #{order.id}'}, status=status.HTTP_200_OK)