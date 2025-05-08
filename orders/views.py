from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.template.loader import get_template, render_to_string
from django.core.mail import EmailMessage
from io import BytesIO
from xhtml2pdf import pisa
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer


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
        order = Order.objects.select_related('customer__user') \
            .prefetch_related('items__product') \
            .get(id=order_id, customer__user=request.user)
    except Order.DoesNotExist:
        return Response({'detail': 'Order not found or access denied.'}, status=status.HTTP_404_NOT_FOUND)

    if order.is_paid:
        return Response({'detail': 'This order is already paid.'}, status=status.HTTP_400_BAD_REQUEST)

    # Update order status
    order.is_paid = True
    order.status = 'completed'
    order.save()

    # Generate invoice PDF using xhtml2pdf
    template = get_template('orders/invoice.html')
    html = template.render({'order': order})
    result = BytesIO()
    pisa_status = pisa.CreatePDF(src=html, dest=result)

    if pisa_status.err:
        return Response({'detail': 'PDF generation failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    pdf = result.getvalue()

    # Prepare email
    email_subject = f"Order Confirmation - #{order.id}"
    email_body = render_to_string("emails/order_confirmation.html", {
        'order': order,
        'customer_name': order.customer.user.first_name or order.customer.user.username,
        'total_price': sum(item.quantity * item.unit_price for item in order.items.all())
    })

    email = EmailMessage(
        subject=email_subject,
        body=email_body,
        from_email="no-reply@espamarket.com",
        to=[order.customer.user.email]
    )
    email.content_subtype = "html"
    email.attach(f"invoice_order_{order.id}.pdf", pdf, "application/pdf")
    email.send()

    return Response({'detail': f'Order #{order.id} marked as paid and confirmation email sent.'}, status=status.HTTP_200_OK)


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
