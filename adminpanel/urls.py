from django.urls import path
from . import admin_views

app_name = 'adminpanel'

urlpatterns = [
    path('dashboard/', admin_views.AdminDashboardView.as_view(), name='dashboard'),
    path('export-data/', admin_views.admin_export_data, name='export_data'),
    path('bulk-actions/', admin_views.admin_bulk_actions, name='bulk_actions'),
]
