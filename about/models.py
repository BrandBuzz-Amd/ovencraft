from django.db import models

class AboutPage(models.Model):
    title = models.CharField(max_length=200, default="About Us")
    subtitle = models.CharField(max_length=300, blank=True)
    hero_content = models.TextField()
    story_title = models.CharField(max_length=200, default="Our Story")
    story_content = models.TextField()
    mission_title = models.CharField(max_length=200, default="Our Mission")
    mission_content = models.TextField()
    vision_title = models.CharField(max_length=200, default="Our Vision")
    vision_content = models.TextField()
    values_title = models.CharField(max_length=200, default="Our Values")
    values_content = models.TextField()
    hero_image = models.ImageField(upload_to='about/', blank=True, null=True)
    story_image = models.ImageField(upload_to='about/', blank=True, null=True)
    team_image = models.ImageField(upload_to='about/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "About Page"
        verbose_name_plural = "About Page"

class Achievement(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    number = models.CharField(max_length=20)
    icon = models.CharField(max_length=50, help_text="Bootstrap icon class")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order', 'title']
