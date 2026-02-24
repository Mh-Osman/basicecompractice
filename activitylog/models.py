# models.py

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from users.models import Customer


class ActivityLog(models.Model):

    ACTION_CHOICES = (
        ("create", "Create"),
        ("update", "Update"),
        ("delete", "Delete"),
    )

    user = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    action = models.CharField(max_length=20, choices=ACTION_CHOICES)

    description = models.TextField(blank=True)

    changes = models.JSONField(null=True, blank=True) 

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]