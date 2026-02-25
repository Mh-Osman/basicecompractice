from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import ActivityLog
from .utils import get_model_changes

# Models to track
MODELS_TO_LOG = ['Product', 'Category', 'Order', 'Customer']

def should_log(sender):
    return sender.__name__ in MODELS_TO_LOG

@receiver(pre_save)
def log_model_update(sender, instance, **kwargs):
    if not should_log(sender) or not instance.pk:
        return

    try:
        old_instance = sender.objects.get(pk=instance.pk)
        changes = get_model_changes(old_instance, instance)
        if changes:
            ActivityLog.objects.create(
                content_type=ContentType.objects.get_for_model(instance),
                object_id=instance.pk,
                action="update",
                changes=changes,
                description=f"{sender.__name__} updated"
            )
    except sender.DoesNotExist:
        pass

@receiver(post_save)
def log_model_create(sender, instance, created, **kwargs):
    if not should_log(sender) or not created:
        return

    ActivityLog.objects.create(
        content_type=ContentType.objects.get_for_model(instance),
        object_id=instance.pk,
        action="create",
        description=f"{sender.__name__} created"
    )

@receiver(post_delete)
def log_model_delete(sender, instance, **kwargs):
    if not should_log(sender):
        return

    ActivityLog.objects.create(
        content_type=ContentType.objects.get_for_model(instance),
        object_id=instance.pk,
        action="delete",
        description=f"{sender.__name__} deleted"
    )