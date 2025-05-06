from django.contrib import admin
from .models import Discount

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['product', 'percentage', 'active', 'start_date', 'end_date']
    list_filter = ['active', 'start_date', 'end_date']
    search_fields = ['product__title']
