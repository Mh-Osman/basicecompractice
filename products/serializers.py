from rest_framework import serializers
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    discount_price = serializers.ReadOnlyField()
    profit = serializers.ReadOnlyField()
    is_low_stock = serializers.ReadOnlyField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'sku', 'barcode', 'supplier', 'category', 'brand', 
            'description', 'cost_price', 'selling_price', 'discount', 
            'stock', 'minimum_stock', 'maximum_stock', 'stock_alarm', 
            'weight', 'dimensions', 'image', 'status', 'is_featured', 
            'created_by', 'created_at', 'updated_at', 
            'discount_price', 'profit', 'is_low_stock'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']