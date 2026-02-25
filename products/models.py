from django.db import models
from users.models import Customer
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Product(models.Model):

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=50, unique=True)
    barcode = models.CharField(max_length=100, blank=True, null=True)

    supplier = models.ForeignKey(
        'users.Customer',  
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )

    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='products'
    )

    brand = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    stock = models.IntegerField(default=0)
    minimum_stock = models.IntegerField(default=0)
    maximum_stock = models.IntegerField(null=True, blank=True)

    stock_alarm = models.IntegerField(default=0) 

    weight = models.FloatField(null=True, blank=True)
    dimensions = models.CharField(max_length=100, blank=True)

    image = models.ImageField(upload_to='product_images/', null=True, blank=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    is_featured = models.BooleanField(default=False)

    created_by = models.ForeignKey(
        'users.Customer',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_products'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def is_low_stock(self):
        return self.stock <= self.minimum_stock

    @property
    def profit(self):
        return self.selling_price - self.cost_price
    
    @property
    def discount_price(self):
        if self.discount:
            return self.selling_price - (self.discount / 100 * self.selling_price)
        return self.selling_price


class ProductEditHistory(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='edit_history')
    previous_data = models.JSONField()
    updated_data = models.JSONField()
    order_id = models.IntegerField(null=True, blank=True)
    updated_by = models.ForeignKey('users.Customer', on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.updated_at} - {self.updated_by}"

class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('in', 'Stock In (Restock)'),
        ('out', 'Stock Out (Sale)'),
        ('adjustment', 'Adjustment'),
        ('return', 'Return'),
    ]

    product = models.ForeignKey(
        'Product', 
        on_delete=models.CASCADE, 
        related_name='stock_movements'
    )
    quantity = models.IntegerField()  
    previous_stock = models.IntegerField()
    new_stock = models.IntegerField()
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    
    
    order = models.ForeignKey(
        'orders.Order', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
   
    performed_by = models.ForeignKey(
        'users.Customer', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True, null=True) 

    def __str__(self):
        return f"{self.product.name} ({self.movement_type}) - Qty: {self.quantity}"
