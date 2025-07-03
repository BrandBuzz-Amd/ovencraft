from django.contrib import admin
from django.utils.html import format_html
from django.http import HttpResponse
import csv
from datetime import datetime
from .models import BlogCategory, Blog, Comment

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'blog_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    actions = ['export_as_csv']

    def blog_count(self, obj):
        return obj.blogs.count()
    blog_count.short_description = 'Number of Blogs'

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename=blog_categories_{datetime.now().strftime("%Y%m%d")}.csv'
        writer = csv.writer(response)
        
        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
        
        return response
    export_as_csv.short_description = "Export selected categories as CSV"

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_published', 'published_at', 'image_preview', 'created_at')
    list_filter = ('is_published', 'categories', 'author', 'created_at')
    search_fields = ('title', 'content', 'excerpt', 'meta_title', 'meta_keywords')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    filter_horizontal = ('categories',)
    date_hierarchy = 'created_at'
    list_editable = ('is_published',)
    actions = ['make_published', 'make_draft', 'export_as_csv', 'duplicate_blogs']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'categories')
        }),
        ('Content', {
            'fields': ('excerpt', 'content')
        }),
        ('Media', {
            'fields': ('featured_image', 'image_preview')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Publishing', {
            'fields': ('is_published', 'published_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def image_preview(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" style="max-height: 100px;" />', obj.featured_image.url)
        return "No image"
    image_preview.short_description = "Featured Image Preview"

    def make_published(self, request, queryset):
        updated = queryset.update(is_published=True, published_at=datetime.now())
        self.message_user(request, f'{updated} blogs were successfully published.')
    make_published.short_description = "Publish selected blogs"

    def make_draft(self, request, queryset):
        updated = queryset.update(is_published=False, published_at=None)
        self.message_user(request, f'{updated} blogs were successfully moved to drafts.')
    make_draft.short_description = "Move selected blogs to drafts"

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename=blogs_{datetime.now().strftime("%Y%m%d")}.csv'
        writer = csv.writer(response)
        
        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
        
        return response
    export_as_csv.short_description = "Export selected blogs as CSV"

    def duplicate_blogs(self, request, queryset):
        for blog in queryset:
            blog.pk = None
            blog.title = f"{blog.title} (Copy)"
            blog.slug = f"{blog.slug}-copy"
            blog.is_published = False
            blog.save()
        
        self.message_user(request, f'{queryset.count()} blogs were successfully duplicated.')
    duplicate_blogs.short_description = "Duplicate selected blogs"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'blog', 'content_preview', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at', 'blog')
    search_fields = ('content', 'user__username', 'blog__title')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['approve_comments', 'disapprove_comments', 'export_as_csv']
    list_editable = ('is_approved',)

    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = "Content Preview"

    def approve_comments(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} comments were successfully approved.')
    approve_comments.short_description = "Approve selected comments"

    def disapprove_comments(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} comments were successfully disapproved.')
    disapprove_comments.short_description = "Disapprove selected comments"

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename=comments_{datetime.now().strftime("%Y%m%d")}.csv'
        writer = csv.writer(response)
        
        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
        
        return response
    export_as_csv.short_description = "Export selected comments as CSV"
