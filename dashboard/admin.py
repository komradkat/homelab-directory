from django.contrib import admin
from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Admin interface for Service model"""
    
    list_display = ['name', 'category', 'protocol', 'port', 'is_active', 'order']
    list_filter = ['category', 'protocol', 'is_active']
    search_fields = ['name', 'description']
    list_editable = ['is_active', 'order']
    ordering = ['category', 'order', 'name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category', 'icon_name')
        }),
        ('Connection Details', {
            'fields': ('protocol', 'port')
        }),
        ('Display Settings', {
            'fields': ('is_active', 'order')
        }),
    )
