from django.urls import path
from .views import (
    contact, contact_api, contact_detail_ajax, mark_contact_read,
    mark_contact_unread, contact_stats_ajax
)

urlpatterns = [
    path('', contact, name='contact'),
    path('api/', contact_api, name='contact_api'),
    
    # Admin AJAX URLs
    path('admin/contact/<int:contact_id>/detail/', contact_detail_ajax, name='contact_detail_ajax'),
    path('admin/contact/<int:contact_id>/mark-read/', mark_contact_read, name='mark_contact_read'),
    path('admin/contact/<int:contact_id>/mark-unread/', mark_contact_unread, name='mark_contact_unread'),
    path('admin/contact/stats/', contact_stats_ajax, name='contact_stats_ajax'),
]
