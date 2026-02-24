from django.contrib import admin

# Register your models here.
from .models import Category, Product, ProductEditHistory, StockMovement

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductEditHistory)
admin.site.register(StockMovement)
    