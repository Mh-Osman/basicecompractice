from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Product, ProductEditHistory
from django.forms.models import model_to_dict

@receiver(pre_save, sender=Product)
def capture_old_product_data(sender, instance, **kwargs):
    try:
        instance._old_instance = Product.objects.get(pk=instance.pk)
    except Product.DoesNotExist:
        instance._old_instance = None

@receiver(post_save, sender=Product)
def create_product_edit_history(sender, instance, created, **kwargs):
    from decimal import Decimal
    
    new_data = model_to_dict(instance)
    for key, value in new_data.items():
        if isinstance(value, Decimal):
            new_data[key] = str(value)
        elif key == 'image':
            new_data[key] = str(value) if value else None

    if created:
        # For initial creation, previous_data is empty
        ProductEditHistory.objects.create(
            product=instance,
            previous_data={},
            updated_data=new_data,
            order_id=getattr(instance, '_order_id', None),
            updated_by=getattr(instance, '_updated_by', instance.created_by)
        )
    elif hasattr(instance, '_old_instance') and instance._old_instance:
        old_data = model_to_dict(instance._old_instance)
        for key, value in old_data.items():
            if isinstance(value, Decimal):
                old_data[key] = str(value)
            elif key == 'image':
                old_data[key] = str(value) if value else None
        
        if old_data != new_data:
            ProductEditHistory.objects.create(
                product=instance,
                previous_data=old_data,
                updated_data=new_data,
                order_id=getattr(instance, '_order_id', None),
                updated_by=getattr(instance, '_updated_by', None)
            )
