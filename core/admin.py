from django.contrib import admin
from django.utils.html import format_html
from django.http import HttpResponse
import csv
from datetime import datetime
from .models import (
    SiteSettings, HeroSection, Testimonial, Partner, 
    AboutContent, TeamMember, Feature
)

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'contact_email', 'contact_phone', 'logo_preview')
    readonly_fields = ('updated_at', 'logo_preview', 'favicon_preview')
    fieldsets = (
        ('Site Information', {
            'fields': ('site_name', 'site_tagline', 'site_description')
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'contact_phone', 'contact_address')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'instagram_url', 'twitter_url', 'linkedin_url', 'youtube_url')
        }),
        ('Media', {
            'fields': ('logo', 'logo_preview', 'favicon', 'favicon_preview')
        }),
        ('System', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        })
    )

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.logo.url)
        return "No logo"
    logo_preview.short_description = "Logo Preview"

    def favicon_preview(self, obj):
        if obj.favicon:
            return format_html('<img src="{}" style="max-height: 32px;" />', obj.favicon.url)
        return "No favicon"
    favicon_preview.short_description = "Favicon Preview"

    def has_add_permission(self, request):
        # Allow only one instance of SiteSettings
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'updated_at', 'preview_link')
    list_filter = ('is_active',)
    search_fields = ('title', 'subtitle', 'description')
    readonly_fields = ('created_at', 'updated_at', 'preview_link')
    list_editable = ('is_active',)
    actions = ['make_active', 'make_inactive', 'duplicate_hero_sections']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'subtitle', 'description', 'button_text', 'button_link')
        }),
        ('Media', {
            'fields': ('background_video', 'background_image')
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
        ('Preview', {
            'fields': ('preview_link',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def preview_link(self, obj):
        return format_html('<a href="/" target="_blank">Preview on Homepage</a>')
    preview_link.short_description = "Preview"

    def make_active(self, request, queryset):
        # First deactivate all hero sections
        HeroSection.objects.update(is_active=False)
        # Then activate selected ones
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} hero sections were successfully activated.')
    make_active.short_description = "Activate selected hero sections"

    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} hero sections were successfully deactivated.')
    make_inactive.short_description = "Deactivate selected hero sections"

    def duplicate_hero_sections(self, request, queryset):
        for hero in queryset:
            hero.pk = None
            hero.title = f"{hero.title} (Copy)"
            hero.is_active = False
            hero.save()
        self.message_user(request, f'{queryset.count()} hero sections were successfully duplicated.')
    duplicate_hero_sections.short_description = "Duplicate selected hero sections"

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'rating', 'is_featured', 'is_active', 'order')
    list_filter = ('rating', 'is_featured', 'is_active')
    search_fields = ('name', 'company', 'content')
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    list_editable = ('order', 'is_featured', 'is_active')
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Image Preview"

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo_preview', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at', 'logo_preview')
    list_editable = ('order', 'is_active')
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.logo.url)
        return "No logo"
    logo_preview.short_description = "Logo Preview"

@admin.register(AboutContent)
class AboutContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at')
    readonly_fields = ('updated_at', 'main_image_preview', 'team_image_preview')
    fieldsets = (
        ('Main Content', {
            'fields': ('title', 'subtitle', 'content')
        }),
        ('Additional Content', {
            'fields': ('mission', 'vision', 'values')
        }),
        ('Media', {
            'fields': ('main_image', 'main_image_preview', 'team_image', 'team_image_preview')
        }),
        ('System', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        })
    )
    
    def main_image_preview(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" style="max-height: 100px;" />', obj.main_image.url)
        return "No image"
    main_image_preview.short_description = "Main Image Preview"
    
    def team_image_preview(self, obj):
        if obj.team_image:
            return format_html('<img src="{}" style="max-height: 100px;" />', obj.team_image.url)
        return "No image"
    team_image_preview.short_description = "Team Image Preview"

    def has_add_permission(self, request):
        # Allow only one instance of AboutContent
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'image_preview', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('name', 'position', 'bio')
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    list_editable = ('order', 'is_active')
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Image Preview"

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('order', 'is_active')
