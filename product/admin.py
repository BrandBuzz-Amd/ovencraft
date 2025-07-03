from django.contrib import admin
from django.utils.html import format_html
from django.http import HttpResponse
import csv
from datetime import datetime
from .models import ProductCategory, Product, ProductImage, ProductSpecification

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Preview"

class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'sale_price', 'stock_quantity', 'is_featured', 'is_active', 'image_preview')
    list_filter = ('category', 'is_featured', 'is_active', 'created_at')
    search_fields = ('name', 'description', 'short_description', 'meta_keywords')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    inlines = [ProductImageInline, ProductSpecificationInline]
    list_editable = ('is_featured', 'is_active', 'stock_quantity')
    actions = ['make_active', 'make_inactive', 'make_featured', 'remove_featured', 'export_as_csv', 'duplicate_products']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'short_description', 'description')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'sale_price', 'stock_quantity')
        }),
        ('Media', {
            'fields': ('main_image', 'image_preview')
        }),
        ('Product Details', {
            'fields': ('features', 'specifications', 'weight', 'dimensions', 'warranty_period')
        }),
        ('SEO Information', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_featured', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def image_preview(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.main_image.url)
        return "No image"
    image_preview.short_description = "Main Image Preview"
    
    # Bulk Actions
    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} products were successfully marked as active.')
    make_active.short_description = "Mark selected products as active"
    
    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} products were successfully marked as inactive.')
    make_inactive.short_description = "Mark selected products as inactive"
    
    def make_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} products were successfully marked as featured.')
    make_featured.short_description = "Mark selected products as featured"
    
    def remove_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} products were successfully removed from featured.')
    remove_featured.short_description = "Remove selected products from featured"
    
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={meta}.csv'
        writer = csv.writer(response)
        
        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])
        
        return response
    export_as_csv.short_description = "Export selected products as CSV"
    
    def duplicate_products(self, request, queryset):
        for product in queryset:
            # Create a copy of the product
            product.pk = None
            product.name = f"{product.name} (Copy)"
            product.slug = f"{product.slug}-copy"
            product.save()
        
        self.message_user(request, f'{queryset.count()} products were successfully duplicated.')
    duplicate_products.short_description = "Duplicate selected products"

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt_text', 'is_primary', 'image_preview')
    list_filter = ('is_primary', 'created_at')
    search_fields = ('product__name', 'alt_text')
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Preview"

@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'value')
    list_filter = ('product',)
    search_fields = ('product__name', 'name', 'value')
