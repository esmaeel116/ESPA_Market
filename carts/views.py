from rest_framework import viewsets, permissions
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


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
