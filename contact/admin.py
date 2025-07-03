from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
import json
from .models import Contact, VisitorTracking, Newsletter

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read', 'newsletter_subscription')
    list_filter = ('is_read', 'newsletter_subscription', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    actions = ['mark_as_read', 'mark_as_unread']

    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Message Details', {
            'fields': ('subject', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'newsletter_subscription')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def changelist_view(self, request, extra_context=None):
        # Get additional statistics for the template
        today = timezone.now().date()
        
        extra_context = extra_context or {}
        extra_context.update({
            'unread_count': Contact.objects.filter(is_read=False).count(),
            'today_count': Contact.objects.filter(created_at__date=today).count(),
        })
        
        return super().changelist_view(request, extra_context=extra_context)

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected messages as unread"

@admin.register(VisitorTracking)
class VisitorTrackingAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'page_visited', 'device_type', 'browser', 'visited_at')
    list_filter = ('device_type', 'browser', 'visited_at')
    search_fields = ('ip_address', 'page_visited', 'user_agent')
    readonly_fields = ('visited_at',)
    date_hierarchy = 'visited_at'
    ordering = ('-visited_at',)

    fieldsets = (
        ('Visitor Information', {
            'fields': ('ip_address', 'user_agent', 'device_type', 'browser')
        }),
        ('Visit Details', {
            'fields': ('page_visited', 'referrer', 'session_key')
        }),
        ('Location', {
            'fields': ('country', 'city')
        }),
        ('Timestamp', {
            'fields': ('visited_at',)
        })
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        # Get visitor statistics
        stats = VisitorTracking.get_visitor_stats()
        
        # Prepare data for pie charts
        device_stats = (VisitorTracking.objects
            .values('device_type')
            .annotate(count=Count('id'))
            .order_by('-count'))
        
        browser_stats = (VisitorTracking.objects
            .values('browser')
            .annotate(count=Count('id'))
            .order_by('-count'))

        # Convert stats to JSON for JavaScript
        extra_context = extra_context or {}
        extra_context.update({
            'visitor_stats': stats,
            'device_stats': json.dumps(list(device_stats)),
            'browser_stats': json.dumps(list(browser_stats)),
        })
        
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'is_active', 'subscribed_at')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email', 'name')
    readonly_fields = ('subscribed_at', 'unsubscribed_at')
    date_hierarchy = 'subscribed_at'
    ordering = ('-subscribed_at',)
    actions = ['activate_subscriptions', 'deactivate_subscriptions']

    fieldsets = (
        ('Subscriber Information', {
            'fields': ('email', 'name')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('subscribed_at', 'unsubscribed_at'),
            'classes': ('collapse',)
        })
    )

    def activate_subscriptions(self, request, queryset):
        queryset.update(is_active=True, unsubscribed_at=None)
    activate_subscriptions.short_description = "Activate selected subscriptions"

    def deactivate_subscriptions(self, request, queryset):
        queryset.update(is_active=False, unsubscribed_at=timezone.now())
    deactivate_subscriptions.short_description = "Deactivate selected subscriptions"
