from django.db import models
from users.models import Customer
# Create your models here.

class SupplierProfile(models.Model):
    user = models.OneToOneField(
        Customer, 
        on_delete=models.CASCADE,
        related_name='supplier_profile'
        )
    company_name = models.CharField(max_length=100)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name