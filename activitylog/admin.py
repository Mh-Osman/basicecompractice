from django.contrib import admin
from .models import ActivityLog

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'user', 'content_type', 'object_id', 'action', 'description']
    list_filter = ['action', 'content_type', 'created_at']
    search_fields = ['description', 'changes']

# Register your models here.
