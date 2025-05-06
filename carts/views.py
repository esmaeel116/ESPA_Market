from rest_framework import viewsets, permissions
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from orders.models import Order, OrderItem, Coupon
from customers.models import Customer
from django.utils import timezone

class CartViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def get_object(self):
        return get_object_or_404(Cart, user=self.request.user)


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def perform_create(self, serializer):
        cart = self.request.user.cart
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']
        serializer.save(
            cart=cart,
            unit_price=product.price,
            quantity=quantity
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout(request):
    user = request.user

    try:
        cart = user.cart
        cart_items = cart.items.select_related('product')
    except Cart.DoesNotExist:
        return Response({'detail': 'Cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

    if not cart_items.exists():
        return Response({'detail': 'Your cart has no items.'}, status=status.HTTP_400_BAD_REQUEST)

    coupon_code = request.data.get('coupon')
    coupon = None
    if coupon_code:
        try:
            coupon = Coupon.objects.get(
                code=coupon_code,
                active=True,
                start_date__lte=timezone.now(),
                end_date__gte=timezone.now()
            )
        except Coupon.DoesNotExist:
            return Response({'detail': 'Invalid or expired coupon.'}, status=status.HTTP_400_BAD_REQUEST)

    order = Order.objects.create(
        customer=user.customer,
        status='pending',
        is_paid=False,
        coupon=coupon
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            unit_price=item.unit_price
        )

    cart.items.all().delete()

    return Response({'detail': f'Order #{order.id} created successfully.'}, status=status.HTTP_201_CREATED)