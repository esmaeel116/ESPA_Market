from django.db import models
from django.utils import timezone
from products.models import Product
from customers.models import Customer


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, help_text="e.g. 10 for 10% discount")
    active = models.BooleanField(default=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def is_valid(self):
        now = timezone.now()
        return self.active and self.start_date <= now <= self.end_date

    def __str__(self):
        return f"{self.code} - {self.discount_percentage}%"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f'Order #{self.pk} - {self.customer}'

    def get_total_price(self):
        return sum(item.quantity * item.unit_price for item in self.items.all())

    def get_discount_amount(self):
        if self.coupon and self.coupon.is_valid():
            return (self.get_total_price() * self.coupon.discount_percentage) / 100
        return 0

    def get_final_price(self):
        return self.get_total_price() - self.get_discount_amount()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.product.title} x {self.quantity}'
