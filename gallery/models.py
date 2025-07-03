
from django.db import models
from django.conf import settings

class MediaType(models.TextChoices):
    IMAGE = "image", "Image"
    VIDEO = "video", "Video"

class GalleryCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class GalleryItem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    file_path = models.FileField(upload_to='gallery/')
    thumbnail_path = models.ImageField(upload_to='gallery/thumbnails/', blank=True, null=True)
    media_type = models.CharField(max_length=10, choices=MediaType.choices)
    category = models.ForeignKey(GalleryCategory, null=True, blank=True, on_delete=models.SET_NULL, related_name="items")
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="gallery_items")

    def __str__(self):
        return self.title
