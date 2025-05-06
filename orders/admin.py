from django.contrib import admin
from .models import Order, OrderItem, Coupon

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'status', 'created_at', 'is_paid']
    list_filter = ['status', 'is_paid', 'created_at']
    search_fields = ['customer__user__username', 'status']
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'unit_price']
    search_fields = ['order__id', 'product__title']

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_percentage', 'active', 'start_date', 'end_date']
    list_filter = ['active', 'start_date', 'end_date']
    search_fields = ['code']
