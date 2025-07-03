from django.contrib import admin
from django.utils.html import format_html
from django.http import HttpResponse
import csv
from datetime import datetime
from .models import FAQCategory, FAQ

@admin.register(FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'is_active', 'faq_count', 'preview_link')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at', 'preview_link')
    ordering = ('order', 'name')
    list_editable = ('order', 'is_active')
    actions = ['make_active', 'make_inactive', 'export_as_csv']

    def faq_count(self, obj):
        return obj.faqs.count()
    faq_count.short_description = 'Number of FAQs'

    def preview_link(self, obj):
        return format_html('<a href="/faq/#{}" target="_blank">View on FAQ Page</a>', obj.slug)
    preview_link.short_description = "Preview"

    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} categories were successfully activated.')
    make_active.short_description = "Activate selected categories"

    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} categories were successfully deactivated.')
    make_inactive.short_description = "Deactivate selected categories"

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename=faq_categories_{datetime.now().strftime("%Y%m%d")}.csv'
        writer = csv.writer(response)
        
        writer.writerow(field_names + ['FAQ Count'])
        for obj in queryset:
            row_data = [getattr(obj, field) for field in field_names]
            row_data.append(obj.faqs.count())
            writer.writerow(row_data)
        
        return response
    export_as_csv.short_description = "Export selected categories as CSV"

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'order', 'is_active', 'answer_preview')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('question', 'answer')
    readonly_fields = ('created_at', 'updated_at', 'answer_preview')
    ordering = ('category', 'order', 'question')
    list_editable = ('order', 'is_active')
    actions = ['make_active', 'make_inactive', 'export_as_csv', 'duplicate_faqs']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'question', 'answer', 'answer_preview')
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def answer_preview(self, obj):
        if obj.answer:
            preview = obj.answer[:100] + "..." if len(obj.answer) > 100 else obj.answer
            return format_html('<div style="max-width: 300px; word-wrap: break-word;">{}</div>', preview)
        return "No answer"
    answer_preview.short_description = "Answer Preview"

    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} FAQs were successfully activated.')
    make_active.short_description = "Activate selected FAQs"

    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} FAQs were successfully deactivated.')
    make_inactive.short_description = "Deactivate selected FAQs"

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename=faqs_{datetime.now().strftime("%Y%m%d")}.csv'
        writer = csv.writer(response)
        
        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
        
        return response
    export_as_csv.short_description = "Export selected FAQs as CSV"

    def duplicate_faqs(self, request, queryset):
        for faq in queryset:
            faq.pk = None
            faq.question = f"{faq.question} (Copy)"
            faq.is_active = False
            faq.save()
        
        self.message_user(request, f'{queryset.count()} FAQs were successfully duplicated.')
    duplicate_faqs.short_description = "Duplicate selected FAQs"

    class Media:
        css = {
            'all': ('css/admin.css',)
        }
        js = ('js/admin.js',)
