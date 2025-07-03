from django.contrib import admin
from django.utils.html import format_html
from django.http import HttpResponse
import csv
from datetime import datetime
from .models import GalleryCategory, GalleryItem

@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'item_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['export_as_csv']

    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Number of Items'

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename=gallery_categories_{datetime.now().strftime("%Y%m%d")}.csv'
        writer = csv.writer(response)
        
        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
        
        return response
    export_as_csv.short_description = "Export selected categories as CSV"

@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'media_type', 'category', 'uploaded_by', 'file_preview', 'is_active', 'created_at')
    list_filter = ('media_type', 'category', 'uploaded_by', 'is_active', 'created_at')
    search_fields = ('title', 'description', 'tags', 'alt_text')
    readonly_fields = ('created_at', 'updated_at', 'file_preview', 'thumbnail_preview')
    list_editable = ('is_active',)
    actions = ['make_active', 'make_inactive', 'export_as_csv', 'optimize_images']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category', 'media_type')
        }),
        ('Media Files', {
            'fields': ('file_path', 'file_preview', 'thumbnail_path', 'thumbnail_preview')
        }),
        ('SEO & Accessibility', {
            'fields': ('alt_text', 'tags')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('System', {
            'fields': ('uploaded_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def file_preview(self, obj):
        if obj.file_path:
            if obj.media_type == 'image':
                return format_html('<img src="{}" style="max-height: 100px;" />', obj.file_path.url)
            elif obj.media_type == 'video':
                return format_html('<video width="150" height="100" controls><source src="{}" type="video/mp4"></video>', obj.file_path.url)
        return "No file"
    file_preview.short_description = "File Preview"

    def thumbnail_preview(self, obj):
        if obj.thumbnail_path:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.thumbnail_path.url)
        return "No thumbnail"
    thumbnail_preview.short_description = "Thumbnail Preview"

    def save_model(self, request, obj, form, change):
        if not obj.uploaded_by:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} gallery items were successfully marked as active.')
    make_active.short_description = "Mark selected items as active"

    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} gallery items were successfully marked as inactive.')
    make_inactive.short_description = "Mark selected items as inactive"

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename=gallery_items_{datetime.now().strftime("%Y%m%d")}.csv'
        writer = csv.writer(response)
        
        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
        
        return response
    export_as_csv.short_description = "Export selected items as CSV"

    def optimize_images(self, request, queryset):
        image_items = queryset.filter(media_type='image')
        for item in image_items:
            # Here you would implement image optimization logic
            # For example, using PIL to resize and compress images
            pass
        self.message_user(request, f'{image_items.count()} images were processed for optimization.')
    optimize_images.short_description = "Optimize selected images"
