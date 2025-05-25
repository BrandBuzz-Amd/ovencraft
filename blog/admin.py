from django.contrib import admin
from .models import BlogCategory, Blog, Comment

admin.site.register(BlogCategory)
admin.site.register(Blog)
admin.site.register(Comment)
