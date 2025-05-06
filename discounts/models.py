from django.db import models
from products.models import Product
from django.utils import timezone

class Discount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='discounts')
    percentage = models.DecimalField(max_digits=5, decimal_places=2, help_text="e.g., 10 for 10% discount")
    active = models.BooleanField(default=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        ordering = ['-start_date']
        verbose_name = "Discount"
        verbose_name_plural = "Discounts"

    def is_valid(self):
        """Check if discount is currently active and within date range."""
        now = timezone.now()
        return self.active and self.start_date <= now <= self.end_date

    def __str__(self):
        return f"{self.percentage}% discount for {self.product.title}"
