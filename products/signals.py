from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Product, ProductEditHistory, StockMovement
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
        
    # --- Stock Movement Tracking ---
    # Retrieve order and performer from instance attributes (set in views)
    order_id = getattr(instance, '_order_id', None)
    order = None
    if order_id:
        from orders.models import Order
        try:
            order = Order.objects.get(id=order_id)
        except (Order.DoesNotExist, ValueError):
            order = None

    performed_by = getattr(instance, '_updated_by', instance.created_by)

    if created:
        # Initial Stock Movement
        StockMovement.objects.create(
            product=instance,
            quantity=instance.stock,
            previous_stock=0,
            new_stock=instance.stock,
            movement_type='in',
            performed_by=performed_by,
            remarks="Initial stock on creation"
        )
    elif hasattr(instance, '_old_instance') and instance._old_instance:
        old_stock = instance._old_instance.stock
        new_stock = instance.stock
        
        if old_stock != new_stock:
            diff = new_stock - old_stock
            mov_type = 'in' if diff > 0 else 'out'
            
            # If it's a sale (linked to an order), its 'out'
            if order:
                mov_type = 'out'
                remarks = f"Sale - Order #{order.id}"
            else:
                remarks = "Manual Adjustment/Restock"

            StockMovement.objects.create(
                product=instance,
                quantity=abs(diff),
                previous_stock=old_stock,
                new_stock=new_stock,
                movement_type=mov_type,
                order=order,
                performed_by=performed_by,
                remarks=remarks
            )

@receiver(post_save, sender=StockMovement)
def broadcast_stock_update(sender, instance, created, **kwargs):
    if created:
        from asgiref.sync import async_to_sync
        from channels.layers import get_channel_layer
        
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'stock_updates',
            {
                'type': 'stock_update',
                'product_name': instance.product.name,
                'quantity': instance.quantity,
                'movement_type': instance.get_movement_type_display(),
                'new_stock': instance.new_stock,
                'timestamp': instance.created_at.strftime('%H:%M:%S')
            }
        )
