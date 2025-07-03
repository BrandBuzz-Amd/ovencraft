                                                      
from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    newsletter_subscription = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

    class Meta:
        ordering = ['-created_at']

class VisitorTracking(models.Model):
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True, null=True)
    page_visited = models.CharField(max_length=255)
    referrer = models.URLField(blank=True, null=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    device_type = models.CharField(max_length=50, blank=True, null=True)  # mobile, desktop, tablet
    browser = models.CharField(max_length=100, blank=True, null=True)
    visited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} - {self.page_visited} - {self.visited_at}"

    class Meta:
        ordering = ['-visited_at']

    @classmethod
    def get_today_visitors(cls):
        today = timezone.now().date()
        return cls.objects.filter(visited_at__date=today).values('ip_address').distinct().count()

    @classmethod
    def get_week_visitors(cls):
        week_ago = timezone.now() - timedelta(days=7)
        return cls.objects.filter(visited_at__gte=week_ago).values('ip_address').distinct().count()

    @classmethod
    def get_month_visitors(cls):
        month_ago = timezone.now() - timedelta(days=30)
        return cls.objects.filter(visited_at__gte=month_ago).values('ip_address').distinct().count()

    @classmethod
    def get_visitor_stats(cls):
        today = cls.get_today_visitors()
        week = cls.get_week_visitors()
        month = cls.get_month_visitors()
        
        return {
            'today': today,
            'week': week,
            'month': month,
            'total': cls.objects.values('ip_address').distinct().count()
        }

class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-subscribed_at']
