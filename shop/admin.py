from django.contrib import admin
from .models import Product, Category, Brand

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
