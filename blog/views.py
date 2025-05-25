from django.shortcuts import render
from .models import Blog

def index(request):
    blogs = Blog.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'blogs.html', {'blogs': blogs})
