from django.contrib import admin
from django.utils.html import format_html
from .models import AboutPage, Achievement

@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at')
    readonly_fields = ('updated_at', 'hero_image_preview', 'story_image_preview', 'team_image_preview')
    fieldsets = (
        ('Hero Section', {
            'fields': ('title', 'subtitle', 'hero_content', 'hero_image', 'hero_image_preview')
        }),
        ('Our Story', {
            'fields': ('story_title', 'story_content', 'story_image', 'story_image_preview')
        }),
        ('Mission & Vision', {
            'fields': (
                'mission_title', 'mission_content',
                'vision_title', 'vision_content'
            )
        }),
        ('Values', {
            'fields': ('values_title', 'values_content')
        }),
        ('Team Section', {
            'fields': ('team_image', 'team_image_preview')
        }),
        ('System', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        })
    )

    def hero_image_preview(self, obj):
        if obj.hero_image:
            return format_html('<img src="{}" style="max-height: 100px;" />', obj.hero_image.url)
        return "No image"
    hero_image_preview.short_description = "Hero Image Preview"

    def story_image_preview(self, obj):
        if obj.story_image:
            return format_html('<img src="{}" style="max-height: 100px;" />', obj.story_image.url)
        return "No image"
    story_image_preview.short_description = "Story Image Preview"

    def team_image_preview(self, obj):
        if obj.team_image:
            return format_html('<img src="{}" style="max-height: 100px;" />', obj.team_image.url)
        return "No image"
    team_image_preview.short_description = "Team Image Preview"

    def has_add_permission(self, request):
        # Allow only one instance of AboutPage
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'number', 'icon', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('title', 'description', 'number')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('order', 'is_active')
    fieldsets = (
        ('Content', {
            'fields': ('title', 'description', 'number')
        }),
        ('Display', {
            'fields': ('icon', 'order', 'is_active')
        }),
        ('System', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
